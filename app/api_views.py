from .serializers import ConcernSerializers
from .models import Concern
from rest_framework import viewsets

class ConcernViewset(viewsets.ModelViewSet):
    queryset = Concern.objects.all()
    serializer_class = ConcernSerializers
    