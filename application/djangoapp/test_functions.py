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

# Test view sending an async stock request (like sent by BI)
def test_api_get_stock(request):
    sendAsyncMsg("gestion-stock", "", "get_stock")
    return HttpResponseRedirect('/')