from django.http import *
from apipkg import api_manager as api
from apipkg import queue_manager as queue
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .utils import *
from datetime import datetime, timedelta
import json
import requests
import logging
import os
from apipkg import api_manager

# Called when an async message asks for the stock status
def async_get_all():
    return

# Called when an async message gives a resupply
def async_resupply(payLoad):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(days=1)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    schedule_task('gestion-stock', '/api/resupply-immediate', 'none', json.dumps(payLoad) , 'Stock: Resupply immediate', time_str)
    return JsonResponse({"Response" : 200})

# Called when an async message asks for a delivery
def async_delivery():
    return