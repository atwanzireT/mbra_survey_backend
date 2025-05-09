from .models import Concern
from rest_framework import serializers

class ConcernSerializers(serializers.ModelSerializer):
    class Meta:
        model = Concern
        fields = [
            'reporter',
            'contact_us',
            'developer_name',
            'zone_or_village',
            'road_name',
            'division',
            'opposite_property_no',
            'structure_photo',
            'submission_date',
        ]