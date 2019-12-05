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
    path('api/resupply', views.api_get_all, name='api-get-all'),
    path('api/delivery', views.api_get_all, name='api-get-all'),
    path('api/add-to-stock-immediate', views.schedule_add_stock, name='add-to-stock'),
    path('api/remove-from-stock-immediate', views.stock_modif, name='get-from-stock'),
]