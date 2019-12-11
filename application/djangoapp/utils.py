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

# Sends an async message
def sendAsyncMsg(to, body, functionName):
    time = api.send_request('scheduler', 'clock/time')
    message = '{ "from":"' + os.environ[
        'DJANGO_APP_NAME'] + '", "to": "' + to + '", "datetime": ' + time + ', "body": ' + json.dumps(
       body) + ', "functionname":"' + functionName + '"}'

    print_info("Send async msg", [
        ("to", to),
        ("body", body),
        ("functionName", functionName),
        ("message", message),
    ])
    queue.send(to, message)

def schedule_task(host, url, recurrence, data, name, time):
    headers = {'Host': 'scheduler'}
    body = {"target_url": url, "target_app": host, "time": time, "recurrence": recurrence, "data": data, "source_app": "gestion-stock", "name": name}
    response = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = body)
    print_info("Schedule task", [
        ("host", host),
        ("url", url),
        ("recurrence", recurrence),
        ("data", data),
        ("name", name),
        ("time", time),
        ("body", body),
        ("response", response)
    ])

def print_info(title, couple_list, should_print=False):
    if not should_print:
        return

    print("\n===== " + title)
    for cl in couple_list:
        print("=== " + cl[0] + ":")
        print(cl[1])
    print("=====\n")