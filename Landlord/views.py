from django.shortcuts import render
from .models import Landlord
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def landlord_home(request):
 return render(request, 'landlord/landlord_home.html')
 