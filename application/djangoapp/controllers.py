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