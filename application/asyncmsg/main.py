import sys
import os
import json
from django.shortcuts import redirect
from apipkg import api_manager

import logging
logging.getLogger("requests").setLevel(logging.ERROR)


from apipkg import queue_manager as queue
sys.dont_write_bytecode = True

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from application.djangoapp.async import *

from application.djangoapp.utils import print_info


def main():
    #FIXME add task to scheduler
    #request = api.send_request('scheduler', 'schedule/add')
    #queue.receive('AppB', callback)
    return

def dispatch(ch, method, properties, body):
    jsonLoad = json.loads(body)
    fromApp = jsonLoad["from"]

    functionName = ""
    if 'functionname' in jsonLoad:
        functionName = jsonLoad["functionname"]

    print_info("Async message received", [
        ("body", body),
        ("jsonLoad", jsonLoad),
        ("fromApp", fromApp),
        ("functionName", functionName)
    ])

    if fromApp == 'gestion-commerciale':
        if functionName == "get_order_stocks":
            async_resupply(jsonLoad["body"])
        elif functionName == "resupply":
            async_resupply(jsonLoad["body"])
        elif functionName == "delivery":
            async_delivery(jsonLoad["body"])
        #else:
        #    print("Le nom de la fonction dans le json n'est pas valide")

    elif fromApp == 'business-intelligence':
        if functionName == "get_stock":
            async_get_stock()
        #else:
        #    print("Le nom de la fonction dans le json n'est pas valide")

    # For testing purpose only
    elif fromApp == 'gestion-stock':
        if functionName == "get_stock":
            async_get_stock()
        #else:
        #    print("Le nom de la fonction dans le json n'est pas valide")

    else:
        print("Le nom de l'application du json n'est pas valide")

if __name__ == '__main__':
    queue.receive('gestion-stock', dispatch)
    main()
