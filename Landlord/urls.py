from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('landlord_home', landlord_home, name='landlord_home'),
    path('landlord_profile/', landlord_profile, name='landlord_profile'),
]
