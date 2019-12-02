import os

from django.apps import AppConfig
from datetime import datetime, timedelta
from apipkg import api_manager as api

myappurl = "http://localhost:" + os.environ["WEBSERVER_PORT"]


class ApplicationConfig(AppConfig):
    name = 'application.djangoapp'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            api.unregister(os.environ['DJANGO_APP_NAME'])
            api.register(myappurl, os.environ['DJANGO_APP_NAME'])

            if 'ENV' in os.environ:
                if os.environ['ENV'] == 'dev':
                    api.post_request(host='scheduler', url='/app/delete?source=gestion-magasin', body={})

            from .views import schedule_task

            clock_time = api.send_request('scheduler', 'clock/time')
            time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
            time = time + timedelta(hours=1)
            time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
            schedule_task('gestion-stock', 'api/request_stock', 'day', '', 'Stock: Daily reappro', time_str)