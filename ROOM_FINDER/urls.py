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
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', homepage, name='homepage'),
    path('landlord/', include('Landlord.urls')),
    path('renter/', include('Renter.urls')),
    path('admin/', admin.site.urls),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
    path('login_as', login_as_view, name='login_as'),
    path('signup_as', signup_as_view, name='signup_as'),
    path('admin_login/', admin_login, name='admin_login'),
    path('landlord_login/', landlord_login, name='landlord_login'),
    path('renter_login/', renter_login, name='renter_login'),
    path('landlord_signup/', landlord_signup, name='landlord_signup'),
    path('renter_signup/', renter_signup, name='renter_signup'),
    path('about/', about_view, name='about'),
    path('manage_renters', manage_renters, name="manage_renters"),
    path('manage_rooms', manage_rooms, name='manage_rooms'),
    path('maanage_landlord', manage_landlords, name="manage_landlords"),
    path('admin_dashboard', admin_dashboard, name='admin_home'),
    path('logout/', Logout, name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)