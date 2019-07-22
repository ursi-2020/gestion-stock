from django.http import HttpResponse
from apipkg import api_manager as api


def index(request):
    info = api.send_request('business-intelligence', 'info')
    return HttpResponse("Je suis gestion des stock et je reçois %r" % info)

def info(request):
    return HttpResponse("Je suis gestion des stocks")

