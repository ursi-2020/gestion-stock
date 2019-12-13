from django.http import *
from apipkg import api_manager as api
from apipkg import queue_manager as queue
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .controllers import *
from .forms import *
from datetime import datetime, timedelta
import json
import requests
import logging
import os
from apipkg import api_manager

# Called when a http request asks for the stock status
@csrf_exempt
def api_get_all(request):
    json = get_stock()
    return HttpResponse(str({"stock": json}))

# Called when a http request gives a resupply
@csrf_exempt
def api_resupply(request):
    ask_for_resupply()
    return JsonResponse({"Response": 200})

# Called when a http request asks for a delivery
@csrf_exempt
def api_delivery(request):
    return JsonResponse({"Response": 200})

# ===== SCHEDULED

# FIXME Update how resupplies and deliveries work

# Called when a scheduled http request gives a resupply
@csrf_exempt
def api_resupply_immediate(request):
    # TODO : check what we're getting from request.body
    order = json.loads(request.body)
    response = stock_modif_from_body(order)
    sendAsyncMsg("gestion-commerciale", response, "get_stock_order_response")
    sendAsyncMsg("business-intelligence", response, "get_resupply")
    return JsonResponse({"Response": response})

# Called when a scheduled http request asks for a delivery
@csrf_exempt
def api_delivery_immediate(request):
    # TODO : check what we're getting from request.body
    order = json.loads(request.body)
    response = stock_modif_from_body(order)
    sendAsyncMsg("gestion-commerciale", response, "get_stock_order_response")
    sendAsyncMsg("business-intelligence", response, "get_delivery")
    return JsonResponse({"Response": response})