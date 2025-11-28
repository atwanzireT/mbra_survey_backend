from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.index, name="index"),

    # Streets
    path('streets/', views.street_road_list, name='street_list'),
    path('streets/create/', views.street_road_create, name='street_create'),
    path('streets/<int:pk>/', views.street_road_detail, name='street_detail'),
    path('streets/<int:pk>/update/', views.street_road_update, name='street_update'),

    # Properties
    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/<int:pk>/update/', views.property_update, name='property_update'),

    # Reports
    path('reports/', views.report_summary, name="report_summary"),

    # Concerns list
    path('concerns/', views.concerns_list, name="concerns_list"),

    # Concerns workflow
    path('concerns/<int:pk>/edit/', views.concern_update, name='concern_update'),
    path('concerns/<int:pk>/approve/', views.approve_concern, name='approve_concern'),
    path('concerns/<int:pk>/defend/', views.defend_concern, name='defend_concern'),

    # Generic success page for street creation
    path('street/success/', views.street_success_view, name='success_url'),
]
