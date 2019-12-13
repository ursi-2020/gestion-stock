from django.urls import path

from . import views, api, test_functions
app_name = 'gestion-stock'
urlpatterns = [
    path('', views.view_index, name='index'),
    path('logs/', views.view_logs, name='logs'),
    path('stock/', views.view_stock, name='stock'),
    path('stock/resupply/', views.view_stock_resupply, name='stock/resupply'),

    ## API ROUTES ##
    path('api/get-all', api.api_get_all, name='api-get-all'),
    path('api/resupply', api.api_resupply, name='api-resupply'),
    path('api/delivery', api.api_delivery, name='api-delivery'),
    path('api/resupply-immediate', api.api_resupply_immediate, name='api-resupply-immediate'),
    path('api/delivery-immediate', api.api_delivery_immediate, name='api-delivery-immediate'),

    ## TESTS ##
    path('test/async_get', test_functions.test_api_get_stock, name='test-api-get-stock')
]