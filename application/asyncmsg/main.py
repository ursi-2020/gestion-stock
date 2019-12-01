import sys
import os
import json
from django.shortcuts import redirect
from apipkg import api_manager


from apipkg import queue_manager as queue
sys.dont_write_bytecode = True

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from application.djangoapp.models import *

from application.djangoapp.views import stock_modif_from_body, sendAsyncMsg


def main():
    #FIXME add task to scheduler
    #request = api.send_request('scheduler', 'schedule/add')
    print("Start")
    #queue.receive('AppB', callback)

def dispatch(ch, method, properties, body):
    print(" [x] Received from queue %r" % body)
    jsonLoad = json.loads(body)
    fromApp = jsonLoad["from"]
    functionName = ""
    if 'functionname' in jsonLoad:
        functionName = jsonLoad["functionname"]

    if fromApp == 'gestion-commerciale':
        if functionName == "get_order_stocks":
            response = stock_modif_from_body(body)
            sendAsyncMsg("gestion-commerciale", response, "get_stock_order_response")
        else:
            print("Le nom de la fonction dans le json n'est pas valide")

    elif fromApp == 'gestion-stock':
        if functionName == "get_order_stocks":
            print("=========== Get order stocks!")
            response = stock_modif_from_body(body)
            sendAsyncMsg("gestion-stock", response, "get_stock_order_response")
        elif functionName == "get_stock_order_response":
            print("=========== Get order stocks response: " + body)
        else:
            print("Le nom de la fonction dans le json n'est pas valide")

    else:
        print("Le nom de l'application du json n'est pas valide")

if __name__ == '__main__':
    queue.receive('gestion-stock', dispatch)
    main()
