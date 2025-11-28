from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

from .data import CELL_CHOICES, DIVISION_CHOICES, WARD_CHOICES

User = get_user_model()


# -----------------------------------
# Concern (Development Concerns)
# -----------------------------------
class Concern(models.Model):
    # Workflow status
    STATUS_NEW = "new"
    STATUS_CONFIRMED = "confirmed"
    STATUS_DEFENDED = "defended"   # ← instead of "rejected"
    STATUS_RESOLVED = "resolved"

    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_DEFENDED, "Defended by Agent"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    # Town agent reaction (approve or defeat)
    AGENT_DECISION_APPROVE = "approve"
    AGENT_DECISION_DEFEAT = "defeat"

    AGENT_DECISION_CHOICES = [
        (AGENT_DECISION_APPROVE, "Approve concern"),
        (AGENT_DECISION_DEFEAT, "Defeat / defend concern"),
    ]

    # Reporter info (citizen / complainant)
    reporter = models.CharField(max_length=50, blank=True, null=True)
    contact_us = models.CharField(max_length=50, blank=True, null=True)

    # Developer / property context
    developer_name = models.CharField(max_length=50, blank=True, null=True)
    zone_or_village = models.CharField(max_length=50, blank=True, null=True)
    road_name = models.CharField(max_length=50, blank=True, null=True)

    # Location – now using choice fields
    division = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=DIVISION_CHOICES,
    )
    ward = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=WARD_CHOICES,
    )
    cell = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=CELL_CHOICES,
    )

    opposite_property_no = models.CharField(max_length=50, blank=True, null=True)

    structure_photo = models.ImageField(
        upload_to="structure_photos",
        blank=True,
        null=True,
    )

    notes = models.CharField(max_length=255, blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    google_maps_link = models.URLField(blank=True, null=True)

    submission_date = models.DateField(auto_now_add=True)

    # 🔹 Linking concern to a Town Agent (assignment)
    assigned_agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="assigned_concerns",
        blank=True,
        null=True,
        help_text="Town agent responsible for handling this concern.",
    )

    # 🔹 Agent reaction (comment + decision)
    agent_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Field agent notes / defence or explanation about the concern.",
    )

    handled_by_agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="handled_concerns",
        blank=True,
        null=True,
        help_text="Town agent who reacted (approved or defeated) this concern.",
    )

    agent_decision = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=AGENT_DECISION_CHOICES,
        help_text="Decision taken by the town agent on this concern.",
    )

    agent_decision_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date & time when the town agent reacted to this concern.",
    )

    # 🔹 Approval / workflow fields (e.g. Planner / Administrator)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="confirmed_concerns",
        blank=True,
        null=True,
        help_text="User (planner/administrator) who confirmed this concern.",
    )
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmation_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notes by the user who confirmed / resolved the concern.",
    )

    class Meta:
        ordering = ["-submission_date"]

    def __str__(self):
        return (
            f"Concern by {self.reporter or 'Unknown'} "
            f"{self.zone_or_village or ''} - {self.road_name or ''} "
            f"on {self.submission_date}"
        )


# -----------------------------------
# Street / Road Information
# -----------------------------------
class StreetRoadInformation(models.Model):
    ROAD_SIGNAGE_CHOICES = (
        ("both", "Both Start And End Signage"),
        ("start", "Starting Signage Only"),
        ("end", "Ending Signage Only"),
        ("no", "No Signage"),
    )

    ROAD_SURFACE_CONDITION = (
        ("tarmacked", "Tarmacked"),
        ("partially_tarmacked", "Partially tarmacked"),
        ("tarmacked_potpoled", "Tarmacked But Potholed"),
        ("gravel_passable", "Gravel and Passable"),
        ("gravel_ditches", "Gravel with Ditches"),
    )

    DRAINAGE_SYSTEM_CHOICES = (
        ("dual_side", "Dual Side Drainage"),
        ("single_side", "Single Side Drainage"),
        ("no_drainage", "No Drainage System"),
        ("partially_dual", "Partially Dual Drainage"),
        ("partially_single", "Partially Single Drainage"),
    )

    PEDESTRIAN_WALKWAY_CHOICES = (
        ("both_sides", "Available on Both Sides"),
        ("one_side", "Available on One Side Only"),
        ("none", "No Walkway"),
        ("encroached", "Encroached or Blocked"),
        ("under_construction", "Under Construction or Repair"),
    )

    CCTV_INFRASTRUCTURE_CHOICES = (
        ("fully_covered", "Fully Covered with CCTV"),
        ("partially_covered", "Partially Covered with CCTV"),
        ("planned", "Planned for Installation"),
        ("not_available", "No CCTV Infrastructure"),
        ("non_functional", "Installed but Non-Functional"),
    )

    STREET_LIGHTING_STATUS_CHOICES = (
        ("fully_functional", "Fully Functional Street Lights"),
        ("partially_functional", "Partially Functional Street Lights"),
        ("non_functional", "Non-Functional Street Lights"),
        ("not_available", "No Street Lighting Available"),
        ("under_installation", "Under Installation or Repair"),
    )

    # Basic identifiers
    street_road_name = models.CharField(max_length=255, blank=True, null=True)

    # 🔹 Used in your form
    village = models.CharField(max_length=255, blank=True, null=True)

    street_road_name_signage = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=ROAD_SIGNAGE_CHOICES,
    )
    starting_point = models.CharField(max_length=255, blank=True, null=True)
    ending_point = models.CharField(max_length=255, blank=True, null=True)

    pedestrian_walkway_status = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=PEDESTRIAN_WALKWAY_CHOICES,
    )
    cctv_infrastructure = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=CCTV_INFRASTRUCTURE_CHOICES,
    )

    # Location – uses your master choices
    division = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=DIVISION_CHOICES,
    )
    ward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=WARD_CHOICES,
    )
    cell = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=CELL_CHOICES,
    )

    area_councilor_name = models.CharField(max_length=255, blank=True, null=True)
    area_councilor_phone_no = models.CharField(max_length=20, blank=True, null=True)

    road_surface_condition = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=ROAD_SURFACE_CONDITION,
    )

    starting_coordinates = models.CharField(max_length=255, blank=True, null=True)
    ending_coordinates = models.CharField(max_length=255, blank=True, null=True)

    street_road_distance = models.CharField(max_length=100, blank=True, null=True)
    no_properties_on_street = models.IntegerField(blank=True, null=True)

    street_lighting_status = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=STREET_LIGHTING_STATUS_CHOICES,
    )

    drainage_system = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=DRAINAGE_SYSTEM_CHOICES,
    )

    service_lane_existence = models.BooleanField(default=False)

    data_entry_date_update = models.DateField(auto_now_add=True)

    notes = models.TextField(blank=True, null=True)

    # 🔹 Link to Town Agent who captured this street/road
    captured_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="captured_streets",
        blank=True,
        null=True,
        help_text="Town agent who captured this street/road information.",
    )

    class Meta:
        ordering = ["division", "ward", "cell", "street_road_name"]
        verbose_name = "Street / Road Information"
        verbose_name_plural = "Streets / Roads Information"

    def __str__(self):
        return self.street_road_name or "Unnamed Street/Road"


# -----------------------------------
# Property Information
# -----------------------------------
class PropertyInformation(models.Model):
    DEVELOPMENT_TYPE_CHOICES = (
        ("modern", "Modern"),
        ("condemned", "Condemned"),
        ("under_construction", "Under Construction"),
        ("vacant", "Vacant"),
        ("delapidated", "Delapidated"),
    )

    PROPERTY_NO_PLATE = (
        ("installed", "Installed"),
        ("reserved", "Reserved"),
        ("allocated", "Allocated"),
    )

    PROPERTY_TYPE_CHOICES = [
        ("residential_owner", "Residential (Owner Occupied only)"),
        ("residential_rented", "Residential (Rented)"),
        ("residential_owner_tenants", "Residential (Owner with Tenants)"),
        ("learning_institution", "Learning Institution"),
        ("industrial", "Industrial"),
        ("warehouse", "Warehouse"),
        ("place_of_worship", "Place of Worship"),
        ("court_of_law", "Court of Law"),
        ("health_facility", "Health Facility"),
        ("storage", "Storage (Warehouse)"),
        ("commercial", "Commercial (Shops, Banks, Bars, Petrol)"),
        ("other", "Other"),
        ("none", "None"),
    ]

    FENCING_TYPE_CHOICES = [
        ("wall_with_gate", "Wall with gate"),
        ("wall_no_gate", "Wall with no gate"),
        ("hedge_with_gate", "Hedge with Gate"),
        ("hedge_no_gate", "Hedge with no gate"),
        ("wooden_fence_gate", "Wooden fence with Gate"),
        ("wooden_fence_no_gate", "Wooden fence no Gate"),
        ("barbed_wire_gate", "Barbed wire with gate"),
        ("barbed_wire_no_gate", "Barbed wire with no gate"),
        ("iron_sheet_fence_gate", "Iron sheet fence with gate"),
        ("iron_sheet_fence_no_gate", "Iron sheet fence with no gate"),
        ("no_fence_no_gate", "No fence no gate"),
    ]

    ROAD_RESERVE_MINIMUM_CHOICES = (
        ("observed", "Observed"),
        ("partially_observed", "Partially Observed"),
        ("not_observed", "Not Observed"),
    )

    # Basic property information
    property_no = models.CharField(max_length=100, blank=True, null=True)
    street = models.ForeignKey(StreetRoadInformation, on_delete=models.CASCADE)

    # Property characteristics
    property_number_plate = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=PROPERTY_NO_PLATE,
    )
    development_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=DEVELOPMENT_TYPE_CHOICES,
    )
    fencing_gate_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=FENCING_TYPE_CHOICES,
    )
    property_usage = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=PROPERTY_TYPE_CHOICES,
    )
    road_reserve_minimum = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=ROAD_RESERVE_MINIMUM_CHOICES,
    )

    # Enhanced location fields
    property_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Human-readable address",
    )
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # 🔹 To match your form widget "coordinates"
    coordinates = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional raw coordinate string (e.g. from GPS).",
    )

    # Property usage details
    no_units_on_property = models.PositiveIntegerField(blank=True, null=True)
    no_users_occupants = models.PositiveIntegerField(blank=True, null=True)

    # Ownership information
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    owner_phone_no = PhoneNumberField(blank=True, null=True)
    owner_email = models.EmailField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)

    # 🔹 Link to Town Agent who captured this property
    captured_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="captured_properties",
        blank=True,
        null=True,
        help_text="Town agent who captured this property information.",
    )

    class Meta:
        ordering = ["property_no"]
        indexes = [
            models.Index(fields=["property_no"]),
            models.Index(fields=["street"]),
            models.Index(fields=["property_usage"]),
        ]
        verbose_name = "Property Information"
        verbose_name_plural = "Property Information"

    def __str__(self):
        return f"{self.property_no} - {self.street or 'Unnamed'}"

    # --- Google Maps helpers ---
    def get_google_maps_url(self):
        """Generate Google Maps URL from coordinates"""
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return None

    def get_google_maps_embed_url(self):
        """Generate Google Maps embed URL for iframes"""
        if self.latitude and self.longitude:
            return (
                f"https://maps.google.com/maps?q={self.latitude},"
                f"{self.longitude}&z=15&output=embed"
            )
        return None

    def get_google_maps_link(self):
        """Generate HTML link to Google Maps"""
        url = self.get_google_maps_url()
        if url:
            return mark_safe(f'<a href="{url}" target="_blank">View on Google Maps</a>')
        return "No location data"

    def get_google_maps_embed(self):
        """Generate HTML embed for Google Maps"""
        url = self.get_google_maps_embed_url()
        if url:
            return mark_safe(
                '<iframe width="100%" height="300" frameborder="0" style="border:0" '
                f'src="{url}" allowfullscreen></iframe>'
            )
        return "No location data available for embedding"

    def save(self, *args, **kwargs):
        """
        Auto-update property_location if we have coordinates but no address.
        (You can replace this with real reverse geocoding later.)
        """
        if self.latitude and self.longitude and not self.property_location:
            self.property_location = f"Lat: {self.latitude}, Long: {self.longitude}"
        super().save(*args, **kwargs)
