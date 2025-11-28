from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Concern, StreetRoadInformation, PropertyInformation
from .serializers import (
    ConcernSerializer,
    StreetRoadInformationSerializer,
    PropertyInformationSerializer,
)


class ConcernViewset(viewsets.ModelViewSet):
    queryset = Concern.objects.all()
    serializer_class = ConcernSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        """
        Save the Concern instance.
        (Email sending has been removed as requested.)
        """
        serializer.save()


class StreetRoadInformationViewSet(viewsets.ModelViewSet):
    queryset = StreetRoadInformation.objects.all()
    serializer_class = StreetRoadInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        street_name = self.request.query_params.get('street_name')
        if street_name:
            queryset = queryset.filter(street_road_name__icontains=street_name)
        return queryset


class PropertyInformationViewSet(viewsets.ModelViewSet):
    queryset = PropertyInformation.objects.all()
    serializer_class = PropertyInformationSerializer
    # Changed from IsAuthenticated to AllowAny (keeping your change)
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        property_no = self.request.query_params.get('property_no')
        street_id = self.request.query_params.get('street_id')

        if property_no:
            queryset = queryset.filter(property_no__icontains=property_no)
        if street_id:
            queryset = queryset.filter(street__id=street_id)
        return queryset


class StreetRoadPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertyInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        street_id = self.kwargs['street_id']
        return PropertyInformation.objects.filter(street__id=street_id)


class StreetRoadUpdateAPIView(generics.UpdateAPIView):
    queryset = StreetRoadInformation.objects.all()
    serializer_class = StreetRoadInformationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PropertyInformationUpdateAPIView(generics.UpdateAPIView):
    queryset = PropertyInformation.objects.all()
    serializer_class = PropertyInformationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
