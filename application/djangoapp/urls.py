from django.urls import path

from . import views
app_name = 'gestion-stock'
urlpatterns = [
    path('', views.view_index, name='index'),
    path('logs/', views.view_logs, name='logs'),
    path('list/', views.view_products, name='list'),
    path('list/update', views.view_products_update, name='list_update'),
    path('list/delete', views.view_products_delete, name='list_delete'),
    path('stock/', views.view_stock, name='stock'),
    path('request_resupply/', views.view_stock_resupply, name='request_resupply'),

    ## API ROUTES ##
    path('api/get-all', views.api_get_all, name='api-get-all'),
    path('api/add-to-stock', views.schedule_add_stock, name='add-to-stock'),
    path('api/entry_delivery', views.stock_modif, name='entry_delivery'),
    path('api/get-from-stock', views.stock_modif, name='get-from-stock'),
    path('api/stock_modif', views.stock_modif, name='get-from-stock'),
    path('api/request_stock', views.request_stock, name='request_stock')
]