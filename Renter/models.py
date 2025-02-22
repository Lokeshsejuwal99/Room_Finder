from django.db import models
from django.contrib.auth.models import User
from Landlord.models import Room

class Renter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='renter')
    contact_number = models.CharField(max_length=15)
    preferred_location = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='renter_pictures/', null=True, blank=True)
    is_renter = models.BooleanField(default=True, null=True)
    
    def __str__(self):
        return self.user.username
       


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True, null=True)
    move_in_date = models.DateField()
    rental_duration = models.CharField(help_text="Duration in months", max_length=40)
    payment_status = models.BooleanField(default=False)
    approved = models.BooleanField(default=False, null=True)
    
    
    def save(self, *args, **kwargs):
        """Override save method to mark room as unavailable upon booking."""
        if self.pk is None:
            self.room.is_available = False
            self.room.save()
        super().save(*args, **kwargs)
    
    
    def delete(self, *args, **kwargs):
     """Override delete method to mark room as available again upon booking cancellation."""
     self.room.is_available = True
     self.room.save()
     super().delete(*args, **kwargs)


    def __str__(self):
        return f"Booking by {self.renter.user.username} for {self.room.title}"
    
    

class Review(models.Model):
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews", null=True)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            if self.room:
                return f"Review for {self.room.title} by {self.name}"
            return f"General Feedback by {self.name}"