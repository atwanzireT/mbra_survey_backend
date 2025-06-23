from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('streets/', views.street_road_list, name='street_list'),
    path('streets/create/', views.street_road_create, name='street_create'),
    path('streets/<int:pk>/', views.street_road_detail, name='street_detail'),
    path('streets/<int:pk>/update/', views.street_road_update, name='street_update'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/<int:pk>/update/', views.property_update, name='property_update'),
    path('reports/', views.report_summary, name="report_summary"),
    path('concerns/', views.concerns_list, name="report_summary"),
    path('street/success/', views.street_success_view, name='success_url'),
]