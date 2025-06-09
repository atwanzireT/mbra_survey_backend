from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ConcernViewset

router = DefaultRouter()
router.register(r'concerns', ConcernViewset)

urlpatterns = [
    path('', include(router.urls))
]