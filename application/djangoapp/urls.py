from django.urls import path

from . import views
app_name = 'gestion-stock'
urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('list/', views.data, name='list'),
    path('list/update', views.view_list_update, name='list_update'),
    path('list/delete', views.list_delete, name='list_delete'),
    path('schedule/add', views.add_schedule, name='add_schedule'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/demo', views.demo_schedule, name='demo-schedule'),
    path('stock/', views.stock, name='stock'),
    path('entries/', views.entry, name='entry'),
    path('test/', views.test, name='test'),
    path('test_async/', views.test_async, name='test_async'),
    path('request_stock/', views.request_stock, name='request_stock'),

    ## API ROUTES ##
    path('api/get-all', views.api_get_all, name='api-get-all'),
    path('api/add-to-stock', views.schedule_add_stock, name='add-to-stock'),
    path('api/entry_delivery', views.stock_modif, name='entry_delivery'),
    path('api/get-from-stock', views.stock_modif, name='get-from-stock'),
    path('api/stock_modif', views.stock_modif, name='get-from-stock'),
    path('api/request_stock', views.request_stock, name='request_stock')
]