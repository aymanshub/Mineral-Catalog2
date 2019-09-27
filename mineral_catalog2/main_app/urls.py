from django.urls import path

from . import views

app_name = 'minerals'

urlpatterns = [
    path('', views.mineral_list, name='list'),
    path('minerals-by-letter/<letter>/', views.mineral_list, name='list'),
    path('mineral/<pk>/', views.mineral_detail, name='detail'),
    path('search/', views.search, name='search'),
]
