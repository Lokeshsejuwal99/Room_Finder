"""
URL configuration for ROOM_FINDER project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .views import *
from Renter.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', homepage, name='homepage'),
    path('landlord/', include('Landlord.urls')),
    path('renter/', include('Renter.urls')),
    
    path('admin/', admin.site.urls),
    path('feedbacks/', feedback_view, name='feedbacks'),
    path('about/', about_view, name='about'),
    path('login_as', login_as_view, name='login_as'),
    path('signup_as', signup_as_view, name='signup_as'),
    path('admin_login/', admin_login, name='admin_login'),
    path('landlord_login/', landlord_login, name='landlord_login'),
    path('renter_login/', renter_login, name='renter_login'),
    path('landlord_signup/', landlord_signup, name='landlord_signup'),
    path('renter_signup/', renter_signup, name='renter_signup'),
    path('admin_manage_rooms', admin_manage_rooms, name="admin_manage_rooms"),
    path('manage_renters', manage_renters, name="manage_renters"),
    path('maanage_landlord', manage_landlords, name="manage_landlords"),
    path('delete_landlord/<int:landlord_id>/', delete_landlord, name='delete_landlord'),
    path('all_bookings/', all_bookings, name='all_bookings'),
    path('delete_renter/<int:renter_id>/', delete_renter, name='delete_renter'),
    path('admin_dashboard', admin_dashboard, name='admin_home'),
    path('room/<int:room_id>/', room_details, name='room_detail'),
    path('admin_feedbacks/', admin_feedbacks, name='admin_feedbacks'),
    path('admin_feedbacks/<int:feedback_id>/', feedback_detail, name='feedback_detail'),
    path('logout/', Logout, name='logout'),
    path('payment/<int:id>/', book_room, name='initiate_payment'),
    path("success/move_in_date/<str:move_in_date>/rental_duration/<str:rental_duration>/room_id/<int:room_id>/", payment_success, name="esewa_success"),
        # path('success/name/<str:name>/email/<str:email>/room_id/<int:room_id>/phone/<str:phone>/', payment_success, name='esewa_success'),
    path('failure/', payment_failure, name='esewa_failure'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    