from django.http import *
from .controllers import *
import logging

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False

# Test view sending an async stock request (like sent by BI)
def test_api_get_stock(request):
    sendAsyncMsg("gestion-stock", "", "get_stock")
    return HttpResponseRedirect('/')