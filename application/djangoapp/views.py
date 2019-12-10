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
