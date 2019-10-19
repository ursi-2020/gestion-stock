import sys
import os
sys.dont_write_bytecode = True

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from application.djangoapp.models import *
from apipkg import api_manager as api

import datetime

def main():
    #FIXME add task to scheduler
    #request = api.send_request('scheduler', 'schedule/add')
    print("Start")

if __name__ == '__main__':
    main()
