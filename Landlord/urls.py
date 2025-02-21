from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('landlord_home', landlord_home, name='landlord_home'),
    path('landlord_profile/', landlord_profile, name='landlord_profile'),
    path('post-room/', post_room, name='post_room'),
    path('manage-rooms/', manage_rooms, name='manage_rooms'),
    path('delete-room/<int:room_id>/', delete_room, name='delete_room'),
    path('edit-room/<int:room_id>/', edit_room, name='edit_room'),
    path('landlord/applications/', view_applications, name='view_applications'),
    path('upload-room-image/<int:room_id>/', upload_room_image, name='upload_room_image'),

]
