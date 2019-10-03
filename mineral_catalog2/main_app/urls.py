from django.urls import path

from . import views


app_name = 'minerals'

urlpatterns = [
    path('', views.mineral_list,
         name='list'
         ),
    path('by-letter/<letter>/', views.mineral_list,
         name='list_by_letter'
         ),
    path('by-category/<selected_category>/', views.mineral_list,
         name='list_by_category'
         ),
    path('by-streak/<selected_streak>/', views.mineral_list,
         name='list_by_streak'
         ),
    path('mineral/<pk>/', views.mineral_detail,
         name='detail'
         ),
    path('search/', views.search,
         name='search'
         ),
]
