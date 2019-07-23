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
    return HttpResponse("Je suis gestion des stocks")

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save()
            return HttpResponseRedirect('/')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form' : form})

def list(request):
    datas = Article.objects.all()
    context = {
        'articles': datas,
    }
    return render(request, "data.html", context)
