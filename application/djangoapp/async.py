from django.http import *
from apipkg import api_manager as api
from .utils import *
from datetime import datetime, timedelta
import json

import logging
logging.getLogger("requests").setLevel(logging.ERROR)

# Called when an async message asks for the stock status (called by business-intelligence)
def async_get_stock():
    json = get_stock()
    sendAsyncMsg("business-intelligence", str({"stock": json}), "get_stock")
    return JsonResponse({"Response" : 200})

# Called when an async message gives a resupply (called by gestion-commerciale)
def async_resupply(payLoad):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(minutes=1)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    schedule_task('gestion-stock', '/api/resupply-immediate', 'none', json.dumps(payLoad) , 'Stock: Resupply immediate', time_str)
    return JsonResponse({"Response" : 200})

# Called when an async message asks for a delivery (called by gestion-commerciale)
def async_delivery(payLoad):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(days=1)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    schedule_task('gestion-stock', '/api/delivery-immediate', 'none', json.dumps(payLoad) , 'Stock: Delivery immediate', time_str)
    return JsonResponse({"Response" : 200})