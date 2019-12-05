from django.http import *
from apipkg import api_manager as api
from apipkg import queue_manager as queue
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .utils import *
from .api import *
from datetime import datetime, timedelta
import json
import requests
import logging
import os
from apipkg import api_manager

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False

# Returns the stock status
def get_stock():
    return

# Returns the stock status for a specific product
def get_product(id):
    return

# Adds a resupply to the stock
def add_to_stock():
    return

# Removes a delivery from the stock
def remove_from_stock():
    return

# Sends an async message to gestion-commerciale to ask for resupply
def ask_for_resupply():
    allStock = api_get_all()
    sendAsyncMsg('gestion-commerciale', allStock, "get_stock")

# Gets all the products from catalogue and stores them
def fetch_products_list():
    product = api.send_request('catalogue-produit', 'api/get-all')
    logger.info("GET host : catalogue-produit at route /api/get-all")

    catalogue = {}
    try:
        catalogue = json.loads(product)
    except:
        return False

    products = catalogue['produits']
    for item in products:
        product_code = item['codeProduit']
        try:
            instance = Produit.objects.get(codeProduit=product_code)
        except Produit.DoesNotExist:
            instance = None
        if instance is not None:
            instance.prix = int(item['prix'])/100
            instance.packaging = item['packaging']
            instance.familleProduit = item["familleProduit"]
            instance.descriptionProduit = item["descriptionProduit"]
            instance.quantiteMin = item["quantiteMin"]
            instance.exclusivite = item["exclusivite"]
            instance.save()
            logger.info("Product " + instance.codeProduit + " has been updated" )
        else:
            Produit.objects.create(
                codeProduit=product_code,
                familleProduit=item["familleProduit"],
                descriptionProduit=item["descriptionProduit"],
                quantiteMin=item["quantiteMin"],
                packaging=item["packaging"],
                prix=int(item["prix"])/100,
                exclusivite=item["exclusivite"]
            )
            logger.info("Product " + product_code + " has been created")
    return True

# Empties the products list
def delete_poducts_list():
    Produit.objects.all().delete()