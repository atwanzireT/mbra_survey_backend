from rest_framework import serializers
from .models import Concern, StreetRoadInformation, PropertyInformation


class ConcernSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concern
        fields = [
            'reporter',
            'contact_us',
            'developer_name',
            'zone_or_village',
            'road_name',
            'division',
            'ward',
            'cell',
            'opposite_property_no',
            'structure_photo',
            'notes',
            'latitude',
            'longitude',
            'google_maps_link',
            'submission_date',
        ]
        read_only_fields = ['submission_date']


class StreetRoadInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreetRoadInformation
        fields = '__all__'

class PropertyInformationSerializer(serializers.ModelSerializer):
    street_name = serializers.CharField(source='street.street_road_name', read_only=True)
    
    class Meta:
        model = PropertyInformation
        fields = '__all__'
        extra_fields = ['street_name']