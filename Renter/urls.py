from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('renter_home', renter_home, name='renter_home'),
    path('book/<int:room_id>/', book_room, name='book_room'),
    path('renter_profile/', renter_profile, name='renter_profile'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('view_bookings/', view_bookings, name="view_bookings"),

]
