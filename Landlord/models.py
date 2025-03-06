from django.db import models
from django.contrib.auth.models import User

class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='landlord_pictures/', null=True, blank=True)
    is_landlord = models.BooleanField(default=True, null=True)
    
    def __str__(self):
        return self.user.username


class Room(models.Model):
    
    ROOM_TYPE = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Flat', 'Flat'),
    ]
    
    owner = models.ForeignKey(Landlord, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    description = models.TextField()
    room_type = models.CharField(choices=ROOM_TYPE, max_length=10, null=True, default="Single")
    is_available = models.BooleanField(default=True)      
    image = models.ManyToManyField('RoomImage', related_name='rooms')
    total_booked_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)

    
    def __str__(self):
        return self.title


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_images/')
    
    def __str__(self):
        return self.room.title

class Payment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")  # The renter making the payment
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="payments")  # The room being booked
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    reference_id = models.CharField(max_length=100, null=True, blank=True)  # eSewa Reference ID after success
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.renter.username} - {self.room.title} - {self.status}"