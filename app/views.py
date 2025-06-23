from django.shortcuts import render, redirect
from .forms import StreetRoadInformationForm, PropertyInformationForm
from .models import Concern
from django.shortcuts import render, redirect, get_object_or_404
from .models import PropertyInformation, StreetRoadInformation
from django.db.models import Count, Sum, FloatField, ExpressionWrapper, F, Q
from django.db.models.functions import Coalesce
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Cast
from django.core.paginator import Paginator


@login_required
def index(request):
    # Basic counts
    concerns = Concern.objects.all()
    streets = StreetRoadInformation.objects.all()
    properties = PropertyInformation.objects.all()
    
    # Time calculations
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    # Concerns statistics
    total_concerns = concerns.count()
    recent_concerns = concerns.filter(submission_date__gte=thirty_days_ago).count()
    concerns_per_division = concerns.values('division').annotate(count=Count('id')).order_by('-count')
    concerns_trend = concerns.annotate(month=TruncMonth('submission_date')).values('month').annotate(
        count=Count('id')).order_by('month')
    
    # Streets statistics
    total_streets = streets.count()
    streets_per_condition = streets.values('road_surface_condition').annotate(
        count=Count('id')).order_by('-count')
    
    # Properties statistics
    total_properties = properties.count()
    total_properties_with_plates = properties.filter(
        ~Q(property_number_plate__isnull=True),
        ~Q(property_number_plate__exact='')
    ).count()
    properties_by_type = properties.values('property_usage').annotate(
        count=Count('id')).order_by('-count')
    
    # Recent activity
    recent_streets = streets.order_by('-data_entry_date_update')[:5]
    recent_properties = properties.order_by('-id')[:5]

    context = {
        # Counts
        'total_concerns': total_concerns,
        'recent_concerns': recent_concerns,
        'total_streets': total_streets,
        'total_properties': total_properties,
        'total_properties_with_plates': total_properties_with_plates,
        
        # Grouped data
        'concerns_per_division': concerns_per_division,
        'streets_per_condition': streets_per_condition,
        'properties_by_type': properties_by_type,
        'concerns_trend': concerns_trend,
        
        # Recent activity
        'recent_streets': recent_streets,
        'recent_properties': recent_properties,
    }
    return render(request, "index.html", context)

@login_required
def street_road_create(request):
    if request.method == 'POST':
        form = StreetRoadInformationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('street_create') 
    else:
        form = StreetRoadInformationForm()
    
    return render(request, 'register-street.html', {'form': form})

@login_required
def street_road_detail(request, pk):
    street = get_object_or_404(StreetRoadInformation, pk=pk)
    return render(request, 'street_detail.html', {'street': street})

@login_required
def street_road_update(request, pk):
    street = get_object_or_404(StreetRoadInformation, pk=pk)
    if request.method == 'POST':
        form = StreetRoadInformationForm(request.POST, instance=street)
        if form.is_valid():
            form.save()
            return redirect('street_detail', pk=street.pk)
    else:
        form = StreetRoadInformationForm(instance=street)
    
    return render(request, 'street_form.html', {'form': form, 'street': street})


@login_required
def street_road_list(request):
    # Get all filter parameters
    query = request.GET.get('q', '')
    ward = request.GET.get('ward', '')
    cell = request.GET.get('cell', '')
    road_condition = request.GET.get('road_condition', '')
    drainage = request.GET.get('drainage', '')
    lighting = request.GET.get('lighting', '')
    
    # Start with all streets
    streets = StreetRoadInformation.objects.all()
    
    # Apply filters
    if query:
        streets = streets.filter(
            Q(street_road_name__icontains=query) |
            Q(division__icontains=query) |
            Q(ward__icontains=query) |
            Q(cell__icontains=query) |
            Q(area_councilor_name__icontains=query)
        )
    
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
    
    # Get unique values for dropdowns
    wards = StreetRoadInformation.objects.values_list('ward', flat=True).distinct().order_by('ward')
    cells = StreetRoadInformation.objects.values_list('cell', flat=True).distinct().order_by('cell')
    
    # Pagination
    paginator = Paginator(streets, 25)  # Show 25 streets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'streets': page_obj,
        'search_query': query,
        'selected_ward': ward,
        'selected_cell': cell,
        'selected_road_condition': road_condition,
        'selected_drainage': drainage,
        'selected_lighting': lighting,
        'wards': wards,
        'cells': cells,
        'road_conditions': StreetRoadInformation.ROAD_SURFACE_CONDITION,
        'drainage_systems': StreetRoadInformation.DRAINAGE_SYSTEM_CHOICES,
        'lighting_statuses': StreetRoadInformation.STREET_LIGHTING_STATUS_CHOICES,
    }
    return render(request, 'street_list.html', context)

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyInformationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('property_create')  # Redirect to property list view
    else:
        form = PropertyInformationForm()
    
    return render(request, 'register-property.html', {'form': form})

@login_required
def property_update(request, pk):
    property = get_object_or_404(PropertyInformation, pk=pk)
    if request.method == 'POST':
        form = PropertyInformationForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyInformationForm(instance=property)
    
    return render(request, 'property_form.html', {'form': form})

@login_required
def property_detail(request, pk):
    property = get_object_or_404(PropertyInformation, pk=pk)
    return render(request, 'property_detail.html', {'property': property})

@login_required
def property_list(request):
    query = request.GET.get('q')
    properties = PropertyInformation.objects.all()
    
    if query:
        properties = properties.filter(
            Q(property_no__icontains=query) |
            Q(street__street_road_name__icontains=query) |
            Q(owner_name__icontains=query) |
            Q(property_usage__icontains=query) |
            Q(development_type__icontains=query)
        )
    
    context = {
        'properties': properties,
        'search_query': query
    }
    return render(request, 'property_list.html', context)




@login_required
def report_summary(request):
    # Road data aggregation
    road_data = (
        StreetRoadInformation.objects
        .values('division', 'ward', 'cell')
        .annotate(
            total_roads=Count('id'),
            total_length=Sum(
                Cast('street_road_distance', output_field=FloatField())
            ),
            tarmacked=Count('id', filter=Q(road_surface_condition='tarmacked')),
            partially_tarmacked=Count('id', filter=Q(road_surface_condition='partially_tarmacked')),
            potpoled=Count('id', filter=Q(road_surface_condition='tarmacked_potpoled')),
            gravel_passable=Count('id', filter=Q(road_surface_condition='gravel_passable')),
            gravel_ditches=Count('id', filter=Q(road_surface_condition='gravel_ditches')),
            lit=Count('id', filter=Q(street_lighting_status='fully_functional')),
            partially_lit=Count('id', filter=Q(street_lighting_status='partially_functional')),
            unlit=Count('id', filter=Q(street_lighting_status='non_functional')),
            no_lighting=Count('id', filter=Q(street_lighting_status='not_available')),
            under_construction=Count('id', filter=Q(street_lighting_status='under_installation')),
            dual_drainage=Count('id', filter=Q(drainage_system='dual_side')),
            single_drainage=Count('id', filter=Q(drainage_system='single_side')),
            no_drainage=Count('id', filter=Q(drainage_system='no_drainage')),
        )
        .order_by('division', 'ward', 'cell')
    )

    # Property data aggregation
    property_data = (
        PropertyInformation.objects
        .values('street__division', 'street__ward', 'street__cell')
        .annotate(
            total_properties=Count('id'),
            installed_plates=Count('id', filter=Q(property_number_plate='installed')),
            reserved_plates=Count('id', filter=Q(property_number_plate='reserved')),
            allocated_plates=Count('id', filter=Q(property_number_plate='allocated')),
            modern_developments=Count('id', filter=Q(development_type='modern')),
            condemned_developments=Count('id', filter=Q(development_type='condemned')),
            construction_developments=Count('id', filter=Q(development_type='under_construction')),
            vacant_developments=Count('id', filter=Q(development_type='vacant')),
            delapidated_developments=Count('id', filter=Q(development_type='delapilated')),
        )
    )

    # Combine data
    combined_data = []
    for road in road_data:
        # Find matching property data
        prop = next((p for p in property_data if 
                    p['street__division'] == road['division'] and
                    p['street__ward'] == road['ward'] and
                    p['street__cell'] == road['cell']), None)
        
        combined = {
            'division': road['division'],
            'ward': road['ward'],
            'cell': road['cell'],
            'road_metrics': road,
            'property_metrics': prop or {}
        }
        combined_data.append(combined)

    # Handle None values when sorting
    wards = sorted({item['ward'] for item in road_data if item['ward'] is not None})
    cells = sorted({item['cell'] for item in road_data if item['cell'] is not None})

    context = {
        'combined_data': combined_data,
        'wards': wards,
        'cells': cells,
    }
    
    return render(request, 'reports.html', context)


@login_required
def concerns_list(requests):
    concerns = Concern.objects.all()
    return render (requests, "concerns.html", {'concerns':concerns})


@login_required
def street_success_view(request):
    return render(request, 'street_success.html')