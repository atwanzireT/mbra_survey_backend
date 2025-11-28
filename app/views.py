from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum, FloatField, Q
from django.db.models.functions import TruncMonth, Cast
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import (
    StreetRoadInformationForm,
    PropertyInformationForm,
    ConcernForm,
)
from .models import Concern, PropertyInformation, StreetRoadInformation


# -----------------------------
# DASHBOARD
# -----------------------------

@login_required
def index(request):
    concerns = Concern.objects.all()
    streets = StreetRoadInformation.objects.all()
    properties = PropertyInformation.objects.all()

    thirty_days_ago = timezone.now().date() - timedelta(days=30)

    # Concerns statistics
    total_concerns = concerns.count()
    recent_concerns = concerns.filter(submission_date__gte=thirty_days_ago).count()
    concerns_per_division = (
        concerns.values("division")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    concerns_trend = (
        concerns.annotate(month=TruncMonth("submission_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    # Approval stats
    pending_concerns = concerns.filter(status=Concern.STATUS_NEW).count()
    confirmed_concerns = concerns.filter(status=Concern.STATUS_CONFIRMED).count()
    defended_concerns = concerns.filter(status=Concern.STATUS_DEFENDED).count()
    resolved_concerns = concerns.filter(status=Concern.STATUS_RESOLVED).count()

    # Streets statistics
    total_streets = streets.count()
    streets_per_condition = (
        streets.values("road_surface_condition")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Properties statistics
    total_properties = properties.count()
    total_properties_with_plates = properties.filter(
        ~Q(property_number_plate__isnull=True),
        ~Q(property_number_plate__exact=""),
    ).count()
    properties_by_type = (
        properties.values("property_usage")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Recent activity
    recent_streets = streets.order_by("-data_entry_date_update")[:5]
    recent_properties = properties.order_by("-id")[:5]

    context = {
        # Counts
        "total_concerns": total_concerns,
        "recent_concerns": recent_concerns,
        "total_streets": total_streets,
        "total_properties": total_properties,
        "total_properties_with_plates": total_properties_with_plates,

        # Approval stats
        "pending_concerns": pending_concerns,
        "confirmed_concerns": confirmed_concerns,
        "defended_concerns": defended_concerns,
        "resolved_concerns": resolved_concerns,

        # Grouped data
        "concerns_per_division": concerns_per_division,
        "streets_per_condition": streets_per_condition,
        "properties_by_type": properties_by_type,
        "concerns_trend": concerns_trend,

        # Recent activity
        "recent_streets": recent_streets,
        "recent_properties": recent_properties,
    }
    return render(request, "index.html", context)


# -----------------------------
# STREET VIEWS
# -----------------------------

@login_required
def street_road_create(request):
    if request.method == "POST":
        form = StreetRoadInformationForm(request.POST)
        if form.is_valid():
            street = form.save(commit=False)
            # link to town agent / user who captured this record
            if hasattr(street, "captured_by"):
                street.captured_by = request.user
            street.save()
            messages.success(request, "Street / road information saved successfully.")
            return redirect("street_create")
    else:
        form = StreetRoadInformationForm()

    return render(request, "register-street.html", {"form": form})


@login_required
def street_road_detail(request, pk):
    street = get_object_or_404(StreetRoadInformation, pk=pk)
    return render(request, "street_detail.html", {"street": street})


@login_required
def street_road_update(request, pk):
    street = get_object_or_404(StreetRoadInformation, pk=pk)
    if request.method == "POST":
        form = StreetRoadInformationForm(request.POST, instance=street)
        if form.is_valid():
            form.save()
            messages.success(request, "Street / road information updated successfully.")
            return redirect("street_detail", pk=street.pk)
    else:
        form = StreetRoadInformationForm(instance=street)

    return render(
        request,
        "street_form.html",
        {"form": form, "street": street},
    )


@login_required
def street_road_list(request):
    query = request.GET.get("q", "")
    division = request.GET.get("division", "")
    ward = request.GET.get("ward", "")
    cell = request.GET.get("cell", "")
    road_condition = request.GET.get("road_condition", "")
    drainage = request.GET.get("drainage", "")
    lighting = request.GET.get("lighting", "")
    signage = request.GET.get("signage", "")
    walkway = request.GET.get("walkway", "")
    cctv = request.GET.get("cctv", "")

    streets = StreetRoadInformation.objects.all()

    if query:
        streets = streets.filter(
            Q(street_road_name__icontains=query)
            | Q(starting_point__icontains=query)
            | Q(ending_point__icontains=query)
            | Q(division__icontains=query)
            | Q(ward__icontains=query)
            | Q(cell__icontains=query)
            | Q(area_councilor_name__icontains=query)
            | Q(notes__icontains=query)
        )

    if division:
        streets = streets.filter(division=division)
    if ward:
        streets = streets.filter(ward=ward)
    if cell:
        streets = streets.filter(cell=cell)
    if road_condition:
        streets = streets.filter(road_surface_condition=road_condition)
    if drainage:
        streets = streets.filter(drainage_system=drainage)
    if lighting:
        streets = streets.filter(street_lighting_status=lighting)
    if signage:
        streets = streets.filter(street_road_name_signage=signage)
    if walkway:
        streets = streets.filter(pedestrian_walkway_status=walkway)
    if cctv:
        streets = streets.filter(cctv_infrastructure=cctv)

    divisions = (
        StreetRoadInformation.objects.values_list("division", flat=True)
        .distinct()
        .order_by("division")
    )
    wards = (
        StreetRoadInformation.objects.values_list("ward", flat=True)
        .distinct()
        .order_by("ward")
    )
    cells = (
        StreetRoadInformation.objects.values_list("cell", flat=True)
        .distinct()
        .order_by("cell")
    )

    total_streets = streets.count()

    paginator = Paginator(streets, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "streets": page_obj,
        "total_streets": total_streets,
        "search_query": query,
        "selected_division": division,
        "selected_ward": ward,
        "selected_cell": cell,
        "selected_road_condition": road_condition,
        "selected_drainage": drainage,
        "selected_lighting": lighting,
        "selected_signage": signage,
        "selected_walkway": walkway,
        "selected_cctv": cctv,
        "divisions": divisions,
        "wards": wards,
        "cells": cells,
        "road_conditions": StreetRoadInformation.ROAD_SURFACE_CONDITION,
        "drainage_systems": StreetRoadInformation.DRAINAGE_SYSTEM_CHOICES,
        "lighting_statuses": StreetRoadInformation.STREET_LIGHTING_STATUS_CHOICES,
        "signage_choices": StreetRoadInformation.ROAD_SIGNAGE_CHOICES,
        "walkway_choices": StreetRoadInformation.PEDESTRIAN_WALKWAY_CHOICES,
        "cctv_choices": StreetRoadInformation.CCTV_INFRASTRUCTURE_CHOICES,
    }
    return render(request, "street_list.html", context)


# -----------------------------
# PROPERTY VIEWS
# -----------------------------

@login_required
def property_create(request):
    if request.method == "POST":
        form = PropertyInformationForm(request.POST)
        if form.is_valid():
            prop = form.save(commit=False)
            # link to capturing town agent / user
            if hasattr(prop, "captured_by"):
                prop.captured_by = request.user
            prop.save()
            messages.success(request, "Property information saved successfully.")
            return redirect("property_create")
    else:
        form = PropertyInformationForm()

    return render(request, "register-property.html", {"form": form})


@login_required
def property_update(request, pk):
    property_obj = get_object_or_404(PropertyInformation, pk=pk)
    if request.method == "POST":
        form = PropertyInformationForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Property information updated successfully.")
            return redirect("property_detail", pk=property_obj.pk)
    else:
        form = PropertyInformationForm(instance=property_obj)

    return render(
        request,
        "property_form.html",
        {"form": form, "property": property_obj},
    )


@login_required
def property_detail(request, pk):
    property_obj = get_object_or_404(PropertyInformation, pk=pk)
    return render(request, "property_detail.html", {"property": property_obj})


@login_required
def property_list(request):
    query = request.GET.get("q", "")
    property_no = request.GET.get("property_no", "")
    street_name = request.GET.get("street_name", "")
    division = request.GET.get("division", "")
    ward = request.GET.get("ward", "")
    cell = request.GET.get("cell", "")
    property_type = request.GET.get("property_type", "")
    development_type = request.GET.get("development_type", "")
    verification_status = request.GET.get("verification_status", "")
    plate_status = request.GET.get("plate_status", "")
    fencing_type = request.GET.get("fencing_type", "")
    road_reserve = request.GET.get("road_reserve", "")

    properties = PropertyInformation.objects.select_related("street").all()

    if query:
        properties = properties.filter(
            Q(property_no__icontains=query)
            | Q(street__street_road_name__icontains=query)
            | Q(owner_name__icontains=query)
            | Q(property_usage__icontains=query)
            | Q(development_type__icontains=query)
            | Q(property_location__icontains=query)
            | Q(owner_phone_no__icontains=query)
            | Q(owner_email__icontains=query)
        )

    if property_no:
        properties = properties.filter(property_no__icontains=property_no)
    if street_name:
        properties = properties.filter(
            street__street_road_name__icontains=street_name
        )
    if division:
        properties = properties.filter(street__division=division)
    if ward:
        properties = properties.filter(street__ward=ward)
    if cell:
        properties = properties.filter(street__cell=cell)
    if property_type:
        properties = properties.filter(property_usage=property_type)
    if development_type:
        properties = properties.filter(development_type=development_type)

    if verification_status == "verified":
        properties = properties.filter(verified=True)
    elif verification_status == "unverified":
        properties = properties.filter(verified=False)

    if plate_status:
        properties = properties.filter(property_number_plate=plate_status)
    if fencing_type:
        properties = properties.filter(fencing_gate_type=fencing_type)
    if road_reserve:
        properties = properties.filter(road_reserve_minimum=road_reserve)

    divisions = (
        StreetRoadInformation.objects.values_list("division", flat=True)
        .distinct()
        .order_by("division")
    )
    wards = (
        StreetRoadInformation.objects.values_list("ward", flat=True)
        .distinct()
        .order_by("ward")
    )
    cells = (
        StreetRoadInformation.objects.values_list("cell", flat=True)
        .distinct()
        .order_by("cell")
    )

    total_properties = properties.count()

    paginator = Paginator(properties, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "properties": page_obj,
        "total_properties": total_properties,
        "search_query": query,
        "property_no": property_no,
        "street_name": street_name,
        "selected_division": division,
        "selected_ward": ward,
        "selected_cell": cell,
        "selected_property_type": property_type,
        "selected_development_type": development_type,
        "selected_verification_status": verification_status,
        "selected_plate_status": plate_status,
        "selected_fencing_type": fencing_type,
        "selected_road_reserve": road_reserve,
        "divisions": divisions,
        "wards": wards,
        "cells": cells,
        "property_types": PropertyInformation.PROPERTY_TYPE_CHOICES,
        "development_types": PropertyInformation.DEVELOPMENT_TYPE_CHOICES,
        "plate_statuses": PropertyInformation.PROPERTY_NO_PLATE,
        "fencing_types": PropertyInformation.FENCING_TYPE_CHOICES,
        "road_reserve_choices": PropertyInformation.ROAD_RESERVE_MINIMUM_CHOICES,
    }
    return render(request, "property_list.html", context)


# -----------------------------
# REPORT SUMMARY
# -----------------------------

@login_required
def report_summary(request):
    road_data = (
        StreetRoadInformation.objects.values("division", "ward", "cell")
        .annotate(
            total_roads=Count("id"),
            total_length=Sum(
                Cast("street_road_distance", output_field=FloatField())
            ),
            tarmacked=Count(
                "id", filter=Q(road_surface_condition="tarmacked")
            ),
            partially_tarmacked=Count(
                "id", filter=Q(road_surface_condition="partially_tarmacked")
            ),
            potpoled=Count(
                "id", filter=Q(road_surface_condition="tarmacked_potpoled")
            ),
            gravel_passable=Count(
                "id", filter=Q(road_surface_condition="gravel_passable")
            ),
            gravel_ditches=Count(
                "id", filter=Q(road_surface_condition="gravel_ditches")
            ),
            lit=Count(
                "id", filter=Q(street_lighting_status="fully_functional")
            ),
            partially_lit=Count(
                "id", filter=Q(street_lighting_status="partially_functional")
            ),
            unlit=Count(
                "id", filter=Q(street_lighting_status="non_functional")
            ),
            no_lighting=Count(
                "id", filter=Q(street_lighting_status="not_available")
            ),
            under_construction=Count(
                "id", filter=Q(street_lighting_status="under_installation")
            ),
            dual_drainage=Count(
                "id", filter=Q(drainage_system="dual_side")
            ),
            single_drainage=Count(
                "id", filter=Q(drainage_system="single_side")
            ),
            no_drainage=Count(
                "id", filter=Q(drainage_system="no_drainage")
            ),
        )
        .order_by("division", "ward", "cell")
    )

    property_data = (
        PropertyInformation.objects.values(
            "street__division", "street__ward", "street__cell"
        )
        .annotate(
            total_properties=Count("id"),
            installed_plates=Count(
                "id", filter=Q(property_number_plate="installed")
            ),
            reserved_plates=Count(
                "id", filter=Q(property_number_plate="reserved")
            ),
            allocated_plates=Count(
                "id", filter=Q(property_number_plate="allocated")
            ),
            modern_developments=Count(
                "id", filter=Q(development_type="modern")
            ),
            condemned_developments=Count(
                "id", filter=Q(development_type="condemned")
            ),
            construction_developments=Count(
                "id", filter=Q(development_type="under_construction")
            ),
            vacant_developments=Count(
                "id", filter=Q(development_type="vacant")
            ),
            delapidated_developments=Count(
                "id", filter=Q(development_type="delapidated")
            ),
        )
    )

    combined_data = []
    for road in road_data:
        prop = next(
            (
                p
                for p in property_data
                if p["street__division"] == road["division"]
                and p["street__ward"] == road["ward"]
                and p["street__cell"] == road["cell"]
            ),
            None,
        )

        combined = {
            "division": road["division"],
            "ward": road["ward"],
            "cell": road["cell"],
            "road_metrics": road,
            "property_metrics": prop or {},
        }
        combined_data.append(combined)

    wards = sorted({item["ward"] for item in road_data if item["ward"] is not None})
    cells = sorted({item["cell"] for item in road_data if item["cell"] is not None})

    context = {
        "combined_data": combined_data,
        "wards": wards,
        "cells": cells,
    }

    return render(request, "reports.html", context)


# -----------------------------
# CONCERNS WORKFLOW
# -----------------------------

@login_required
def concerns_list(request):
    user = request.user
    profile = getattr(user, "profile", None)

    base_qs = Concern.objects.all().order_by("-submission_date")
    pending_concerns = base_qs.filter(status=Concern.STATUS_NEW)
    concerns = base_qs

    if profile:
        if profile.role == "town_agent":
            # Town agent: see concerns assigned to them or handled by them or unassigned
            concerns = concerns.filter(
                Q(assigned_agent=user)
                | Q(handled_by_agent=user)
                | Q(assigned_agent__isnull=True)
            ).filter(
                status__in=[
                    Concern.STATUS_NEW,
                    Concern.STATUS_CONFIRMED,
                    Concern.STATUS_DEFENDED,
                ]
            ).distinct()
            pending_concerns = concerns.filter(status=Concern.STATUS_NEW)

        elif profile.role in ["planner", "administrator"]:
            # Full visibility
            pending_concerns = base_qs.filter(status=Concern.STATUS_NEW)

        else:
            # Other users: only confirmed and resolved
            concerns = concerns.filter(
                status__in=[Concern.STATUS_CONFIRMED, Concern.STATUS_RESOLVED]
            )
            pending_concerns = Concern.objects.none()
    else:
        # No profile – safest: only confirmed & resolved
        concerns = concerns.filter(
            status__in=[Concern.STATUS_CONFIRMED, Concern.STATUS_RESOLVED]
        )
        pending_concerns = Concern.objects.none()

    context = {
        "concerns": concerns,
        "pending_concerns": pending_concerns,
        "user_role": profile.role if profile else None,
    }
    return render(request, "concerns.html", context)


@login_required
def concern_update(request, pk):
    """
    Generic concern reaction/update using ConcernForm.

    - Town Agent:
        • chooses agent_decision (approve/defeat)
        • writes agent_notes
        • system maps decision → status (CONFIRMED / DEFENDED) if concern was NEW.
    - Planner/Admin:
        • can move status through full workflow
        • can add confirmation_notes.
    """
    concern = get_object_or_404(Concern, pk=pk)
    profile = getattr(request.user, "profile", None)

    if not profile:
        return HttpResponseForbidden("You are not allowed to update concerns.")

    if request.method == "POST":
        form = ConcernForm(request.POST, instance=concern, user=request.user)
        if form.is_valid():
            old_status = concern.status
            concern = form.save(commit=False)
            now = timezone.now()

            # Town agent reaction
            if profile.role == "town_agent":
                if not concern.handled_by_agent:
                    concern.handled_by_agent = request.user
                if not concern.agent_decision_at:
                    concern.agent_decision_at = now

                if old_status == Concern.STATUS_NEW:
                    if concern.agent_decision == Concern.AGENT_DECISION_APPROVE:
                        concern.status = Concern.STATUS_CONFIRMED
                    elif concern.agent_decision == Concern.AGENT_DECISION_DEFEAT:
                        concern.status = Concern.STATUS_DEFENDED

            # Planner / Administrator confirmation
            elif profile.role in ("planner", "administrator"):
                if concern.status != old_status and concern.status != Concern.STATUS_NEW:
                    concern.confirmed_by = request.user
                    concern.confirmed_at = now

            concern.save()
            messages.success(request, "Concern updated successfully.")
            return redirect("concerns_list")
    else:
        form = ConcernForm(instance=concern, user=request.user)

    return render(request, "concern_update.html", {"form": form, "concern": concern})


@login_required
def approve_concern(request, pk):
    """
    Quick action: Town Agent approves (confirms) a concern.
    Sets agent_decision = APPROVE, updates status if still NEW.
    """
    concern = get_object_or_404(Concern, pk=pk)
    profile = getattr(request.user, "profile", None)

    if not profile or profile.role != "town_agent":
        return HttpResponseForbidden("You are not allowed to approve concerns.")

    if request.method == "POST":
        notes = request.POST.get("agent_notes", "")

        concern.agent_notes = notes or concern.agent_notes
        concern.agent_decision = Concern.AGENT_DECISION_APPROVE
        concern.handled_by_agent = request.user
        concern.agent_decision_at = timezone.now()

        if concern.status == Concern.STATUS_NEW:
            concern.status = Concern.STATUS_CONFIRMED

        concern.save()

        messages.success(request, "Concern approved (confirmed) successfully.")
        return redirect("concerns_list")

    return render(request, "concern_approve.html", {"concern": concern})


@login_required
def defend_concern(request, pk):
    """
    Quick action: Town Agent defends the concern (no violation).
    Sets agent_decision = DEFEAT, updates status if still NEW.
    """
    concern = get_object_or_404(Concern, pk=pk)
    profile = getattr(request.user, "profile", None)

    if not profile or profile.role != "town_agent":
        return HttpResponseForbidden("You are not allowed to defend concerns.")

    if request.method == "POST":
        notes = request.POST.get("agent_notes", "")

        concern.agent_notes = notes or concern.agent_notes
        concern.agent_decision = Concern.AGENT_DECISION_DEFEAT
        concern.handled_by_agent = request.user
        concern.agent_decision_at = timezone.now()

        if concern.status == Concern.STATUS_NEW:
            concern.status = Concern.STATUS_DEFENDED

        concern.save()

        messages.info(request, "Concern defended successfully.")
        return redirect("concerns_list")

    return render(request, "concern_defend.html", {"concern": concern})


# -----------------------------
# SIMPLE SUCCESS VIEW
# -----------------------------

@login_required
def street_success_view(request):
    return render(request, "street_success.html")
