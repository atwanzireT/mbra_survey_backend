from django.shortcuts import render
from .models import Concern

# Create your views here.
def index(requests):
    concerns = Concern.objects.all()
    return render(requests, "index.html", {'concerns': concerns})