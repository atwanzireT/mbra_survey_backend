from django.contrib import admin
from .models import Concern, StreetRoadInformation, PropertyInformation

# Register your models here.
admin.site.register(Concern)
admin.site.register(StreetRoadInformation)
admin.site.register(PropertyInformation)