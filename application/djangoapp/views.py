from django.http import *
from apipkg import api_manager as api
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import *
from .forms import *

import datetime

def index(request):
    info = api.send_request('business-intelligence', 'info')
    return render(request, "index.html", {'info' : info})

def request(request):
    text = api.send_request('business-intelligence', 'info')
    return HttpResponse(text)

def button(request):
    context = {}
    return render(request, "button.html", context)

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
    datas = api.send_request('catalogueproduit', 'api/data') #Article.objects.all()
    #FIXME check error request
    if datas.status_code > 299 :
        print(datas.status_code)
        #FIXME add nyancat
    context = {
        'articles': datas,
    }
    return render(request, "data.html", context)


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