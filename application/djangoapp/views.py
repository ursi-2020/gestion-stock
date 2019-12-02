from django.http import *
from apipkg import api_manager as api
from apipkg import queue_manager as queue
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import *
from .forms import *
from datetime import datetime, timedelta
import json
import requests
import logging
import os
from apipkg import api_manager


logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False

#Affichage de la page d'accueil
def index(request):
    return render(request, "index.html")

### API
def api_get_all():
    stock = Article.objects.values()
    json = list(stock)
    return {"stock": json}

def request_stock(request):
    print("\n========== Request_stock")
    allStock = api_get_all()
    print("allStock:")
    print(allStock)
    print("==========\n")
    sendAsyncMsg('gestion-commerciale', allStock, "get_stock")
    context = {
        'stock': Article.objects.all(),
    }
    return render(request, "stock.html", context)

#...
def info(request):
    return HttpResponse("Gestion des stocks")

#
def demo_schedule(request):
    print("========== Demo schedule")
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=10)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    schedule_task('gestion-stock', '/list/update','minute','','demo', time_str)
    return HttpResponseRedirect('/schedule')

def stock(request):
    context = {
        'stock': Article.objects.all(),
    }
    return render(request, "stock.html", context)

def entry(request):
    context = {
        'entries': Entry.objects.all(),
    }
    return render(request, "entries.html", context)

@csrf_exempt
def schedule_add_stock(request):
    print("========== Schedule add stock")
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(days=1)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    data = (request.body).decode("utf-8")
    schedule_task('gestion-stock', '/api/entry_delivery', 'none', data , 'schedule_delivery', time_str)
    return JsonResponse({"Response" : 200})

@csrf_exempt
def schedule_stock_modif(payLoad):
    print("\n========== Schedule stock modif")
    print("payLoad:")
    print(payLoad)
    print("JSONified:")
    print(json.dumps(payLoad))
    print("==========\n")
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(days=1)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    schedule_task('gestion-stock', '/api/stock_modif', 'none', json.dumps(payLoad) , 'stock_modif', time_str)
    return JsonResponse({"Response" : 200})

def dict_to_json(py_dict):
    tmp = json.loads(json.dumps(py_dict))
    return tmp

@csrf_exempt
def stock_modif(request):
    print("\n========== Stock modif")
    print("body:")
    print(request.body)
    print("loaded:")
    print(json.loads(request.body))
    print("==========\n")
    # TODO : check what we're getting from request.body
    order = json.loads(request.body)
    response = stock_modif_from_body(order)
    sendAsyncMsg("gestion-commerciale", response, "get_stock_order_response")
    return JsonResponse({"Response": response})

def stock_modif_from_body(order):
    print("========== Stock modif from body")
    livraison = 1 if order["livraison"] else -1
    list = order["produits"]
    # Dictionnary to create Entry object before rendering
    entry = {}
    entry["idCommande"] = order["idCommande"]
    command = []
    newProduct = []
    for produit in list:
        product = {}
        codeProduit = produit["codeProduit"]
        delivered = produit["quantite"]
        try:
            instance = Article.objects.get(codeProduit=codeProduit)
        except Article.DoesNotExist:
            instance = None
        # Object exist in stock
        if instance is not None:
            # GesCo ordered more than what's in stock
            if not order["livraison"] and instance.quantite < produit["quantite"]:
                delivered = 0
            instance.quantite += delivered * livraison
            instance.save()
            logger.info("Article " + str(instance.codeProduit) + " was sucessfully updated : new stock value : " + str(instance.quantite))
        # Object doesn't exist in stock
        else:
            # Requesting object not in base ==> Inserting in base with quantity 0
            if not order["livraison"]:
                delivered = 0
                #newProduct = Article.objects.create(
                 #   codeProduit=codeProduit,
                  #  quantite=produit["quantite"]
                #)
                #logger.info("Article " + str(newProduct.codeProduit) + " was sucessfully created : new stock value : " + str(newProduct.quantite))
            # Handles all other cases (insertion in base)
            newProduct.append(Article(codeProduit=codeProduit, quantite=delivered))
        product["codeProduit"] = codeProduit
        product["quantite"] = delivered
        command.append(product)
    # Bulk Creating articles, trying out solution to fix problem
    Article.objects.bulk_create(newProduct)
    # Creating Entry item for Logs
    entry["produits"] = command
    package = json.dumps(entry, indent=2)
    date = datetime.now()
    Entry.objects.create(
        package=package,
        date=date,
        delivery=True if livraison > 0 else False
    )
    logger.info("Entry created : package was : " + package + ", at : " + date.strftime("%Y-%b-%d, %H:%M:%S"))
    return entry

@csrf_exempt
def test(request):
    print("========== Test")
    #Article.objects.all().delete()
    #Entry.objects.all().delete()
    str = '{"Produits": [{"codeProduit": "X1-0", "quantite": 16}, {"codeProduit": "X1-1", "quantite": 20}, {"codeProduit": "X1-2", "quantite": 21}, {"codeProduit": "X1-3", "quantite": 27}, {"codeProduit": "X1-4", "quantite": 13}, {"codeProduit": "X1-8", "quantite": 20}, {"codeProduit": "X1-9", "quantite": 10}, {"codeProduit": "X1-10", "quantite": 28}], "livraison": 0, "idCommande": 15012019145734}'
    res = api.post_request('gestion-stock', 'api/add-to-stock', str)
    print(res)
    return HttpResponseRedirect('/stock')

def data(request):
    context = {
        'produits': Produit.objects.all(),
    }
    return render(request, "data.html", context)

def list_delete(request):
    Produit.objects.all().delete()
    return HttpResponseRedirect('/list')

@csrf_exempt
def get_product(request):
    product = api.send_request('catalogue-produit', 'api/get-all')
    logger.info(
        "GET host : catalogue-produit at route /api/get-all")
    if product == "An invalid response was received from the upstream server\n":
        return render(request, '404_Not_Found.html')
    else :
        catalogue = json.loads(product)
        list = catalogue['produits']
        for item in list:
            codeProduit = item['codeProduit']
            try:
                instance = Produit.objects.get(codeProduit=codeProduit)
            except Produit.DoesNotExist:
                instance = None
            if instance is not None:
                instance.prix = int(item['prix'])/100
                instance.packaging = item['packaging']
                instance.familleProduit = item["familleProduit"]
                instance.descriptionProduit = item["descriptionProduit"]
                instance.quantiteMin = item["quantiteMin"]
                instance.exclusivite = item["exclusivite"]
                instance.save()
                logger.info("Product " + instance.codeProduit + " a été mis à jour" )
            else:
                Produit.objects.create(
                    codeProduit=codeProduit,
                    familleProduit=item["familleProduit"],
                    descriptionProduit=item["descriptionProduit"],
                    quantiteMin=item["quantiteMin"],
                    packaging=item["packaging"],
                    prix=int(item["prix"])/100,
                    exclusivite=item["exclusivite"]
                )
                logger.info("Product " + codeProduit + " a été créé")
        return HttpResponseRedirect('/list')


def add_schedule(request):
    print("========== Add schedule")
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule_task(form['host'].value(),
                          form['url'].value(),
                          form['recurrence'].value(),
                          form['data'].value(),
                          form['name'].value(),
                          form['time'].value())
            return HttpResponseRedirect('/schedule')
        else:
            form = ScheduleForm()
        return render(request, 'index.html', {'form': form})

def schedule_task(host, url, recurrence, data, name, time):
    print("========== Schedule task")
    headers = {'Host': 'scheduler'}
    body = {"target_url": url, "target_app": host, "time": time, "recurrence": recurrence, "data": data, "source_app": "gestion-stock", "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = body)
    print(r.json())
    print(r.status_code)
    print(r.text)
    return r.text

def schedule(request):
    print("========== Schedule")
    list = api.send_request('scheduler', 'schedule/list')
    time = api.send_request('scheduler', 'clock/time')
    return render(request, "schedule.html", {'list' : list, 'time':time, 'form': ScheduleForm})

#FIXME ajouter le log dans la BDD
def log(request):
    date = datetime.now().strftime('%Y-%m-%d-%H-%M')
    return list(request)

def sendAsyncMsg(to, body, functionName):
    print("\n========== Send async msg")
    print("to: ")
    print(to)
    print("body: ")
    print(body)
    print("functionName: ")
    print(functionName)
    print("============\n")
    time = api.send_request('scheduler', 'clock/time')
    message = '{ "from":"' + os.environ[
        'DJANGO_APP_NAME'] + '", "to": "' + to + '", "datetime": ' + time + ', "body": ' + json.dumps(
       body) + ', "functionname":"' + functionName + '"}'
    queue.send(to, message)

def test_async(request):
    print("=========== Test async call")
    sendAsyncMsg("gestion-stock", "{}", "get_order_stocks")
    return render(request, "index.html", {})
