from django.urls import path

from . import views
app_name = 'gestion-stock'
urlpatterns = [
    path('', views.view_index, name='index'),
    path('logs/', views.view_logs, name='logs'),
    path('stock/', views.view_stock, name='stock'),
    path('stock/resupply/', views.view_stock_resupply, name='stock/resupply'),

    ## API ROUTES ##
    path('api/get-all', views.api_get_all, name='api-get-all'),
    path('api/resupply', views.api_resupply, name='api-resupply'),
    path('api/delivery', views.api_delivery, name='api-delivery'),
    path('api/resupply-immediate', views.api_resupply_immediate, name='api-resupply-immediate'),
    path('api/delivery-immediate', views.api_delivery_immediate, name='api-delivery-immediate'),
]