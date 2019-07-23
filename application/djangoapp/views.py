from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from application.djangoapp.models import *
from .forms import *

import datetime
def index(request):
    info = api.send_request('business-intelligence', 'info')
    return HttpResponse("Je suis gestion des stock et je reçois %r" % info)

def request(request):
    text = api.send_request('business-intelligence', 'info')
    #d = Data.objects.create(text=text, date=datetime.datetime.now())
    return HttpResponse(text)

def button(request):
    context = {}
    return render(request, "button.html", context)

def info(request):
    return HttpResponse("Je suis gestion des stocks")

def list(request):
    datas = Data.objects.all()
    context = {
        'datas': datas
    }
    return render(request, "data.html", context)
