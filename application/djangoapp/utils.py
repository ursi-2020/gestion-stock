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
    print("\n========== Send async msg")
    print("to: ")
    print(to)
    print("body: ")
    print(body)
    print("functionName: ")
    print(functionName)
    time = api.send_request('scheduler', 'clock/time')
    message = '{ "from":"' + os.environ[
        'DJANGO_APP_NAME'] + '", "to": "' + to + '", "datetime": ' + time + ', "body": ' + json.dumps(
       body) + ', "functionname":"' + functionName + '"}'
    print("message: ")
    print(message)
    print("============\n")
    queue.send(to, message)