from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('search/whoisdetails/', views.whoisdetails, name='whoisdetails'),
    path('search/nsdetails/', views.nsdetails, name='nsdetails'),
]
