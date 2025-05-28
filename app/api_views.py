from rest_framework import viewsets
from django.core.mail import send_mail
from .models import Concern
from .serializers import ConcernSerializers
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import EmailMessage
import mimetypes

class ConcernViewset(viewsets.ModelViewSet):
    queryset = Concern.objects.all()
    serializer_class = ConcernSerializers
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        instance = serializer.save()

        # Compose email
        subject = f"New Concern Submitted by {instance.reporter or 'Anonymous'}"
        message = f"""
            A new concern has been submitted:
            Reporter: {instance.reporter}
            Contact: {instance.contact_us}
            Developer: {instance.developer_name}
            Location: {instance.zone_or_village}, {instance.road_name}, {instance.division}
            Opposite Property No: {instance.opposite_property_no}
            Submitted On: {instance.submission_date}

            Please log in to the admin portal to view the full details.
        """
        recipient = [settings.ADMIN_EMAIL]

        # Create EmailMessage object instead of using send_mail
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient,
        )

        # Attach the structure photo if it exists
        if instance.structure_photo:
            try:
                # Open the image file
                with instance.structure_photo.open() as f:
                    # Determine MIME type based on file extension
                    mime_type, _ = mimetypes.guess_type(instance.structure_photo.name)
                    mime_type = mime_type or 'application/octet-stream'  # Default if unknown
                    
                    # Attach the file to the email
                    email.attach(
                        filename=instance.structure_photo.name,
                        content=f.read(),
                        mimetype=mime_type
                    )
            except FileNotFoundError:
                # Handle case where file was saved but doesn't exist physically
                pass  # Or log an error message here

        # Send the email
        email.send(fail_silently=False)