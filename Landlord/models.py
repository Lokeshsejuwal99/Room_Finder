from django.db import models
from django.contrib.auth.models import User

class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='landlord_profile')
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='landlord_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Room(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.BooleanField(default=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='rooms')
    posted_on = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title


class RoomPhoto(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='room_photos/')
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.room.title}"
