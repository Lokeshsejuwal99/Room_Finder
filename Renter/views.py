from django.shortcuts import render
from .models import Renter
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def renter_home(request):
 return render(request, 'renter/renter_home.html')