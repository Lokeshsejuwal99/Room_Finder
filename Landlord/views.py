from django.shortcuts import render
from .models import Landlord
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def landlord_home(request):
 return render(request, 'landlord/landlord_home.html')
 
 
@login_required
def landlord_profile(request):
    landlord = request.user
    context = {
        'landlord': landlord,
    }
    return render(request, 'landlord/land_profile.html', context)