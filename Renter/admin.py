from django.contrib import admin
from .models import Renter, Review, Booking

@admin.register(Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = ['user', 'contact_number', 'preferred_location']
    
admin.site.register(Booking)
admin.site.register(Review)
