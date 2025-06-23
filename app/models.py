from django.db import models
from .data import CELL_CHOICES, DIVISION_CHOICES, WARD_CHOICES

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



class StreetRoadInformation(models.Model):
    ROAD_SIGNAGE_CHOICES = (
        ('both', 'Both Start And End Signage'),
        ('start', 'Starting Signage Only'),
        ('end', 'Ending Signage Only'),
        ('no', 'No Signage'),
    )

    ROAD_SURFACE_CONDITION = (
        ('tarmacked', 'Tarmacked'),
        ('partially_tarmacked', 'Partially tarmacked'),
        ('tarmacked_potpoled', 'Tarmacked But Potpoled'),
        ('gravel_passable', 'Gravel and Passable'),
        ('gravel_ditches', 'Gravel with Ditches'),
    )

    DRAINAGE_SYSTEM_CHOICES = (
        ('dual_side', 'Dual Side Drainage'),
        ('single_side', 'Single Side Drainage'),
        ('no_drainage', 'No Drainage Systemc'),
        ('partially_dual', 'Partially Dual Drainage'),
        ('partially_single', 'Partially Single Drainage')

    )

    PEDESTRIAN_WALKWAY_CHOICES = (
        ('both_sides', 'Available on Both Sides'),
        ('one_side', 'Available on One Side Only'),
        ('none', 'No Walkway'),
        ('encroached', 'Encroached or Blocked'),
        ('under_construction', 'Under Construction or Repair'),
    )

    CCTV_INFRASTRUCTURE_CHOICES = (
        ('fully_covered', 'Fully Covered with CCTV'),
        ('partially_covered', 'Partially Covered with CCTV'),
        ('planned', 'Planned for Installation'),
        ('not_available', 'No CCTV Infrastructure'),
        ('non_functional', 'Installed but Non-Functional'),
    )

    STREET_LIGHTING_STATUS_CHOICES = (
        ('fully_functional', 'Fully Functional Street Lights'),
        ('partially_functional', 'Partially Functional Street Lights'),
        ('non_functional', 'Non-Functional Street Lights'),
        ('not_available', 'No Street Lighting Available'),
        ('under_installation', 'Under Installation or Repair'),
    )


    street_road_name = models.CharField(max_length=255, blank=True, null=True)
    street_road_name_signage = models.CharField(max_length=255, blank=True, null=True, choices=ROAD_SIGNAGE_CHOICES)
    starting_point = models.CharField(max_length=255, blank=True, null=True)
    ending_point = models.CharField(max_length=255, blank=True, null=True)
    pedestrian_walkway_status = models.CharField(max_length=255, blank=True, null=True, choices=PEDESTRIAN_WALKWAY_CHOICES)
    cctv_infrastructure = models.CharField(max_length=255, blank=True, null=True, choices=CCTV_INFRASTRUCTURE_CHOICES)
    division = models.CharField(max_length=255, blank=True, null=True, choices=DIVISION_CHOICES)
    ward = models.CharField(max_length=255, blank=True, null=True, choices=WARD_CHOICES)
    cell = models.CharField(max_length=255, blank=True, null=True, choices=CELL_CHOICES)
    area_councilor_name = models.CharField(max_length=255, blank=True, null=True)
    area_councilor_phone_no = models.CharField(max_length=20, blank=True, null=True)
    road_surface_condition = models.CharField(max_length=255, blank=True, null=True, choices=ROAD_SURFACE_CONDITION)
    starting_coordinates = models.CharField(max_length=255, blank=True, null=True)
    ending_coordinates = models.CharField(max_length=255, blank=True, null=True)
    street_road_distance = models.CharField(max_length=100, blank=True, null=True)
    no_properties_on_street = models.IntegerField(blank=True, null=True)
    street_lighting_status = models.CharField(max_length=255, blank=True, null=True, choices=STREET_LIGHTING_STATUS_CHOICES)
    drainage_system = models.CharField(max_length=255, blank=True, null=True, choices=DRAINAGE_SYSTEM_CHOICES)
    service_lane_existence = models.BooleanField(default=False)
    data_entry_date_update = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.street_road_name or "Unnamed Street/Road"
    

class PropertyInformation(models.Model):
    DEVELOPMENT_TYPE_CHOICES = (
        ('modern', 'Modern'),
        ('condemned', 'Condemned'),
        ('under_construction', 'Under Construction'),
        ('vacant', 'Vacant'),
        ('delapilated', 'Delapilated'),
    )

    PROPERTY_NO_PLATE =(
        ('installed', 'Installed'),
        ('reserved', 'Reserved'),
        ('allocated', 'Allocated'),
    )

    PROPERTY_TYPE_CHOICES = [
        ('residential_owner', 'Residential (Owner Occupied only)'),
        ('residential_rented', 'Residential (Rented)'),
        ('residential_owner_tenants', 'Residential (Owner with Tenants)'),
        ('learning_institution', 'Learning Institution'),
        ('industrial', 'Industrial'),
        ('warehouse', 'Warehouse'),
        ('place_of_worship', 'Place of Worship'),
        ('court_of_law', 'Court of Law'),
        ('health_facility', 'Health Facility'),
        ('storage', 'Storage (Warehouse)'),
        ('commercial', 'Commercial (Shops, Banks, Bars, Petrol)'),
        ('other', 'Other'),
        ('none', 'None'),
    ]

    FENCING_TYPE_CHOICES = [
        ('wall_no_gate', 'Wall with no gate'),
        ('hedge_with_gate', 'Hedge with Gate'),
        ('hedge_no_gate', 'Hedge with no gate'),
        ('wooden_fence_gate', 'Wooden fence with Gate'),
        ('wooden_fence_no_gate', 'Wooden fence no Gate'),
        ('barbed_wire_gate', 'Barbed wire with gate'),
        ('barbed_wire_no_gate', 'Barbed wire with no gate'),
        ('iron_sheet_fence_gate', 'Iron sheet fence with gate'),
        ('iron_sheet_fence_no_gate', 'Iron sheet fence with no gate'),
        ('no_fence_no_gate', 'No fence no gate'),
    ]

    ROAD_RESERVE_MINIMUM_CHOICES = (
        ('observed', 'Observed'),
        ('partially_observed', 'Partially Observed'),
        ('not_observed', 'Not Observed')
    )
    property_no = models.CharField(max_length=100, blank=True, null=True)
    street = models.ForeignKey(StreetRoadInformation, on_delete=models.CASCADE)
    property_number_plate = models.CharField(max_length=100, blank=True, null=True, choices=PROPERTY_NO_PLATE)
    development_type = models.CharField(max_length=100, blank=True, null=True, choices=DEVELOPMENT_TYPE_CHOICES)
    fencing_gate_type = models.CharField(max_length=100, blank=True, null=True, choices=FENCING_TYPE_CHOICES)
    property_usage = models.CharField(max_length=100, blank=True, null=True, choices=PROPERTY_TYPE_CHOICES)
    road_reserve_minimum = models.CharField(max_length=50, blank=True, null=True, choices=ROAD_RESERVE_MINIMUM_CHOICES)
    coordinates = models.CharField(max_length=255, blank=True, null=True)
    no_units_on_property = models.PositiveIntegerField(blank=True, null=True)
    no_users_occupants = models.PositiveIntegerField(blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    owner_phone_no = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.property_no} - {self.street or 'Unnamed'}"