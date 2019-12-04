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

def get_stock():
    return

def get_product(id):
    return

def add_to_stock():
    return

def remove_from_stock():
    return