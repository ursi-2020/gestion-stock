from django.http import *
from apipkg import api_manager as api
from apipkg import queue_manager as queue
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import *
from .forms import *
from .controllers import *
from datetime import datetime, timedelta
import json
import requests
import logging
import os
from apipkg import api_manager

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False

# View of the home page
def view_index(request):
    return render(request, "index.html")

# View displaying the logs
def view_logs(request):
    context = {
        'entries': Entry.objects.all(),
    }
    return render(request, "logs.html", context)

# View showing the stock status
def view_stock(request):
    context = {
        'stock': Article.objects.all(),
    }
    return render(request, "stock.html", context)

# View asking for a resupply
def view_stock_resupply(request):
    ask_for_resupply()
    return HttpResponseRedirect('/stock')

# ===== FIXME DESTROY EVERYTHING AFTER THIS POINT

#Affichage de la page d'accueil
def index(request):
    return render(request, "index.html")

### API
def api_get_all(request):
    stock = Article.objects.values()
    json = list(stock)
    return HttpResponse(str({"stock": json}))

@csrf_exempt
def request_stock(request):
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

@csrf_exempt
def schedule_add_stock(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(days=1)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    data = (request.body).decode("utf-8")
    schedule_task('gestion-stock', '/api/entry_delivery', 'none', data , 'schedule_delivery', time_str)
    return JsonResponse({"Response" : 200})

@csrf_exempt
def schedule_stock_modif(payLoad):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(days=1)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    schedule_task('gestion-stock', '/api/stock_modif', 'none', json.dumps(payLoad) , 'Stock: Modif', time_str)
    return JsonResponse({"Response" : 200})

def dict_to_json(py_dict):
    tmp = json.loads(json.dumps(py_dict))
    return tmp

@csrf_exempt
def stock_modif(request):
    # TODO : check what we're getting from request.body
    order = json.loads(request.body)
    response = stock_modif_from_body(order)
    sendAsyncMsg("gestion-commerciale", response, "get_stock_order_response")
    return JsonResponse({"Response": response})

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

def test_async(request):
    print("=========== Test async call")
    sendAsyncMsg("gestion-stock", "{}", "get_order_stocks")
    return render(request, "index.html", {})
