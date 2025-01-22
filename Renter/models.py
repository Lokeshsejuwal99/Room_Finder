from django.db import models
from django.contrib.auth.models import User
from Landlord.models import Room

class Renter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='renter_profile')
    contact_number = models.CharField(max_length=15)
    preferred_location = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='renter_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username
       
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    payment_status = models.BooleanField(default=False)  # True if payment is completed

    def __str__(self):
        return f"Booking by {self.renter.username} for {self.room.title}"


class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.renter.username} for {self.room.title}"
