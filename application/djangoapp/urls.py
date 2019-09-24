from django.urls import path

from . import views
app_name = 'gestion-stock'
urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('list/', views.list, name='list'),
    path('schedule/add', views.add_schedule, name='add_schedule'),
    path('add-article/', views.add_article, name='add-article'),
    path('remove-article/', views.remove_article, name='remove-article'),
    path('clear/', views.clear, name='clear'),
    path('schedule/', views.schedule, name='schedule'),
]