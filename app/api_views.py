from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from .models import Concern
from .serializers import ConcernSerializer
import mimetypes
import base64
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import StreetRoadInformation, PropertyInformation
from .serializers import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition

class ConcernViewset(viewsets.ModelViewSet):
    queryset = Concern.objects.all()
    serializer_class = ConcernSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        instance = serializer.save()

        # Compose message body
        message_body = f"""
        A new concern has been submitted:

        Reporter: {instance.reporter}
        Contact: {instance.contact_us}
        Developer: {instance.developer_name}
        Division: {instance.division}
        Road Name: {instance.road_name}
        Zone/Village: {instance.zone_or_village}
        Opposite Property No: {instance.opposite_property_no}
        Latitude: {instance.latitude}
        Longitude: {instance.longitude}
        Google Maps: {instance.google_maps_link}
        Notes: {instance.notes}
        Submitted On: {instance.submission_date}

        Please log in to the admin portal to view the full details.
        """.strip()

        # Prepare email
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=[settings.ADMIN_EMAIL],
            subject=f"New Concern Submitted by {instance.reporter or 'Anonymous'}",
            plain_text_content=message_body
        )

        # Attach file if it exists
        if instance.structure_photo:
            try:
                with instance.structure_photo.open('rb') as f:
                    file_data = f.read()
                    encoded_file = base64.b64encode(file_data).decode()
                    mime_type, _ = mimetypes.guess_type(instance.structure_photo.name)
                    mime_type = mime_type or 'application/octet-stream'

                    attachment = Attachment(
                        FileContent(encoded_file),
                        FileName(instance.structure_photo.name),
                        FileType(mime_type),
                        Disposition('attachment')
                    )
                    message.attachment = attachment
            except FileNotFoundError:
                pass

        # Send email with SendGrid
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
        except Exception as e:
            print(f"Error sending email via SendGrid: {e}")


class StreetRoadInformationViewSet(viewsets.ModelViewSet):
    queryset = StreetRoadInformation.objects.all()
    serializer_class = StreetRoadInformationSerializer
    permission_classes = [AllowAny]  # Changed from IsAuthenticated to AllowAny

    def get_queryset(self):
        queryset = super().get_queryset()
        street_name = self.request.query_params.get('street_name', None)
        if street_name:
            queryset = queryset.filter(street_road_name__icontains=street_name)
        return queryset

class PropertyInformationViewSet(viewsets.ModelViewSet):
    queryset = PropertyInformation.objects.all()
    serializer_class = PropertyInformationSerializer
    permission_classes = [AllowAny]  # Changed from IsAuthenticated to AllowAny

    def get_queryset(self):
        queryset = super().get_queryset()
        property_no = self.request.query_params.get('property_no', None)
        street_id = self.request.query_params.get('street_id', None)
        
        if property_no:
            queryset = queryset.filter(property_no__icontains=property_no)
        if street_id:
            queryset = queryset.filter(street__id=street_id)
        return queryset

class StreetRoadPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertyInformationSerializer
    permission_classes = [AllowAny]  # Changed from IsAuthenticated to AllowAny

    def get_queryset(self):
        street_id = self.kwargs['street_id']
        return PropertyInformation.objects.filter(street__id=street_id)

class StreetRoadUpdateAPIView(generics.UpdateAPIView):
    queryset = StreetRoadInformation.objects.all()
    serializer_class = StreetRoadInformationSerializer
    permission_classes = [AllowAny]  # Changed from IsAuthenticated to AllowAny
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class PropertyInformationUpdateAPIView(generics.UpdateAPIView):
    queryset = PropertyInformation.objects.all()
    serializer_class = PropertyInformationSerializer
    permission_classes = [AllowAny]  # Changed from IsAuthenticated to AllowAny
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)