from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('street-road/create/', views.street_road_create, name='street_road_create'),
]