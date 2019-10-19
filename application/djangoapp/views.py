from django.http import *
from apipkg import api_manager as api
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import *
from .forms import *
from datetime import datetime, timedelta
import json
import requests
import logging


logger = logging.getLogger(__name__)

#Affichage de la page d'accueil
def index(request):
    return render(request, "index.html")

### API
def api_get_all(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed
    stock = Article.objects.all()
    jsonData = list(stock.values())
    return JsonResponse({"stock" : jsonData})

#...
def info(request):
    return HttpResponse("Gestion des stocks")

#
def demo_schedule(request):
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
def stock_modif(request):
    # TODO : check what we're getting from request.body
    order = json.loads(request.body)
    livraison = 1 if order["livraison"] else -1
    list = order["Produits"]
    # Dictionnary to create Entry object before rendering
    entry = {}
    entry["idCommande"] = order["idCommande"]
    products = []
    for produit in list:
        product = {}
        codeProduit = produit["codeProduit"]
        try:
            instance = Article.objects.get(codeProduit=codeProduit)
        except Article.DoesNotExist:
            instance = None
        if instance is not None:
            # GesCo ordered more than what's in stock
            if not order["livraison"] and instance.quantity < produit["quantite"]:
                logger.error("Trying to get more of what's in stock")
                return HttpResponse(500)
            instance.quantity += produit["quantite"] * livraison
            instance.save()
            logger.info("Article " + instance.codeProduit + " was sucessfully updated : new stock value : " + instance.quantity)
        else:
            if order["livraison"]:
                Article.objects.create(
                    codeProduit=codeProduit,
                    quantity=produit["quantite"]
                )
                logger.info("Article " + instance.codeProduit + " was sucessfully created : new stock value : " + instance.quantity)
            # A priori, should never be called except if gesco decides to retrieve an item not in stock
            else:
                logger.error("Trying to get an article not in stock")
                return HttpResponse(500)
        product["codeProduit"] = codeProduit
        product["quantite"] = produit["quantite"] * livraison
        products.append(product)
    # Creating Entry item for Logs
    entry["Produits"] = products
    package = json.dumps(entry, indent=2)
    date = datetime.now()
    Entry.objects.create(
        package= package,
        date=date
    )
    logger.info("Entry created : package was : " + package + ", at : " + date.strftime("%Y-%b-%d, %H:%M:%S"))
    return JsonResponse({"Response" : entry})


def list(request):
    context = {
        'articles': Article.objects.all(),
    }
    return render(request, "data.html", context)

def list_delete(request):
    Produit.objects.all().delete()
    return HttpResponseRedirect('/list')

@csrf_exempt
def get_product(request):
    product = api.send_request('catalogue-produit', 'api/data')
    logger.info(
        "GET host : catalogue-produit at route /api/data")
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
                instance.save()
                logger.info("Product " + instance.codeProduit + " a été mis à jour" )
            else:
                Produit.objects.create(
                    codeProduit=codeProduit,
                    familleProduit=item["familleProduit"],
                    descriptionProduit=item["descriptionProduit"],
                    quantiteMin=item["quantiteMin"],
                    packaging=item["packaging"],
                    prix=int(item["prix"])/100
                )
                logger.info("Product " + codeProduit + " a été créé")
        return HttpResponseRedirect('/list')


def add_schedule(request):
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

def schedule_task(host, url, recurrence,data, name, time):
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time, "recurrence": recurrence, "data": data, "source_app": "gestion-stock", "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    print(r.status_code)
    print(r.text)
    return r.text

def schedule(request):
    list = api.send_request('scheduler', 'schedule/list')
    time = api.send_request('scheduler', 'clock/time')
    return render(request, "schedule.html", {'list' : list, 'time':time, 'form': ScheduleForm})



#FIXME ajouter le log dans la BDD
def log(request):
    date = datetime.now().strftime('%Y-%m-%d-%H-%M')
    return list(request)