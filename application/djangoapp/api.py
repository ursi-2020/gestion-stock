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

# Called when a http request asks for the stock status
def api_get_all():
    return

# Called when a http request gives a resupply
def api_resupply():
    return

# Called when a http request asks for a delivery
def api_delivery():
    return

# ===== SCHEDULED

# Called when a scheduled http request gives a resupply
def api_resupply_immediate():
    return

# Called when a scheduled http request asks for a delivery
def api_delivery_immediate():
    return