from django.http import *
from apipkg import api_manager as api
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import *
from .forms import *
from datetime import datetime
import json
import requests
import logging


logger = logging.getLogger(__name__)

def index(request):
    return render(request, "index.html")

def info(request):
    return HttpResponse("Gestion des stocks")

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

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            first = Article.objects.all().filter(nom=form['nom'].value()).first()
            if (first is None) :
                new_article = form.save()
            else :
                first.stock += int(form['stock'].value())
                first.save()
            return HttpResponseRedirect('/list')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form' : form})

def list(request):
    context = {
        'produits': Produit.objects.all(),
    }
    return render(request, "data.html", context)

def list_delete(request):
    Produit.objects.all().delete()
    return HttpResponseRedirect('/list')

@csrf_exempt
def get_product(request):
    product = api.send_request('catalogue-produit', 'catalogueproduit/api/data')
    logger.info(
        "GET host : catalogue-produit at route /catalogueproduit/api/data")
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
        return HttpResponseRedirect('/')


def schedule_task(host, url, recurrence,data, name, time):
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time, "recurrence": recurrence, "data": data, "source_app": "gestion-stock", "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    print(r.status_code)
    print(r.text)
    return r.text

def log(request):
    date = datetime.now().strftime('%Y-%m-%d-%H-%M')
    #FIXME ajouter le log dans la BDD
    return list(request)

def clear(request):
    Article.objects.all().delete()
    return HttpResponseRedirect('/list')

def remove_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            first = Article.objects.all().filter(nom=form['nom'].value()).first()
            if (first is not None) :
                form_stock = int(form['stock'].value())
                if (form_stock > first.stock):
                    first.stock = 0
                else :
                    first.stock -= int(form['stock'].value())
                first.save()
            return HttpResponseRedirect('/list')
    else:
        form = ArticleForm()
    return render(request, 'remove_article.html', {'form' : form})

def schedule(request):
    list = api.send_request('scheduler', 'schedule/list')
    time = api.send_request('scheduler', 'clock/time')
    return render(request, "schedule.html", {'list' : list, 'time':time, 'form': ScheduleForm})

