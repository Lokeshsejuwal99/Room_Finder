from django.contrib import admin
from .models import Landlord, Room, RoomImage

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    list_display = ['user', 'contact_number', 'address']
    
admin.site.register(Room)
admin.site.register(RoomImage)