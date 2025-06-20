from django.shortcuts import render, redirect
from .forms import StreetRoadInformationForm
from .models import Concern

# Create your views here.
def index(requests):
    concerns = Concern.objects.all()
    return render(requests, "index.html", {'concerns': concerns})


def street_road_create(request):
    if request.method == 'POST':
        form = StreetRoadInformationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = StreetRoadInformationForm()
    
    return render(request, 'register-street.html', {'form': form})