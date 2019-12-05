from django.http import *
from apipkg import api_manager as api
from apipkg import queue_manager as queue
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import *
from .forms import *
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
def async_resupply():
    return

# Called when an async message asks for a delivery
def async_delivery():
    return