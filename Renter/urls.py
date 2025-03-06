from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('renter_home', renter_home, name='renter_home'),
    path('renter_profile/', renter_profile, name='renter_profile'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('view_bookings/', view_bookings, name="view_bookings"),
    path('booking-confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('view_rooms', view_rooms, name="view_rooms"),
    path("submit_review/<int:room_id>/", submit_review, name="submit_review"),
    # path('payment-success/', payment_success, name='payment_success'),
    # path('payment-failed/', payment_failure, name='payment_failed'),

]

