from django.db import models

class Concern(models.Model):
    reporter = models.CharField(max_length=50, blank=True, null=True)
    contact_us = models.CharField(max_length=50, blank=True, null=True)
    developer_name = models.CharField(max_length=50, blank=True, null=True)
    zone_or_village = models.CharField(max_length=50, blank=True, null=True)
    road_name = models.CharField(max_length=50, blank=True, null=True)
    division = models.CharField(max_length=50, blank=True, null=True) 
    ward = models.CharField(max_length=50, blank=True, null=True)
    cell = models.CharField(max_length=50, blank=True, null=True)
    opposite_property_no = models.CharField(max_length=50, blank=True, null=True)
    structure_photo = models.ImageField(upload_to="structure_photos", blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    google_maps_link = models.URLField(blank=True, null=True)
    submission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Concern by {self.reporter or 'Unknown'} {self.zone_or_village} - {self.road_name} on {self.submission_date}"
