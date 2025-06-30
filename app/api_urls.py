from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import *

router = DefaultRouter()
router.register(r'concerns', ConcernViewset)
router.register(r'streets', StreetRoadInformationViewSet, basename='street')
router.register(r'properties', PropertyInformationViewSet, basename='property')


urlpatterns = [
    path('', include(router.urls)),
    path('streets/<int:street_id>/properties/', StreetRoadPropertiesAPIView.as_view(), name='street-properties'),
    path('streets/<int:pk>/update/', StreetRoadUpdateAPIView.as_view(), name='street-update'),
    path('properties/<int:pk>/update/', PropertyInformationUpdateAPIView.as_view(), name='property-update'),
]