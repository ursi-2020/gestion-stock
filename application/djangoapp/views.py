from django.http import *
from apipkg import api_manager as api
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import *
from django.contrib.staticfiles.templatetags.staticfiles import static
from .forms import *
from datetime import datetime
import json

def index(request):
    scheduler()
    return render(request, "index.html")

def info(request):
    return HttpResponse("Gestion des stocks")

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
    get_product()
    context = {
        'produits': Produit.objects.all(),
    }
    return render(request, "data.html", context)

def get_product():
    request = api.send_request('catalogue-produit', 'catalogueproduit/api/data')
    catalogue = json.loads(request)
    list = catalogue['produits']
    for item in list:
        codeProduit = item['codeProduit']
        instance = Produit.objects.get(codeProduit=codeProduit)
        if (instance.exist()):
            instance.prix = item['prix']
            instance.packaging = item['packaging']
            instance.familleProduit = item["familleProduit"]
            instance.descriptionProduit = item["descriptionProduit"]
            instance.quantiteMin = item["quantiteMin"]
            instance.save()
        else:
            Produit.objects.create(
                codeProduit=codeProduit,
                familleProduit=item["familleProduit"],
                descriptionProduit=item["descriptionProduit"],
                quantiteMin=item["quantiteMin"],
                packaging=item["packaging"],
                prix=item["prix"]
            )


def scheduler():
    body = open("./static/schedule.json", mode='r', encoding='utf-8')
    data = json.load(body)
    print(data)
    #schedule = api.post_request('scheduler', '/schedule/add', data)
    body.close()


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

