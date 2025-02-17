# from django import forms
# from .models import Booking, Renter

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['move_in_date', 'rental_duration']  # These are the fields for Booking
    
#     # If full_name and phone are part of the Renter model:
#     full_name = forms.CharField(max_length=100)
#     phone = forms.CharField(max_length=15)

#     def clean_full_name(self):
#         return self.cleaned_data['full_name'].strip()

#     def clean_phone(self):
#         return self.cleaned_data['phone'].strip()


from django import forms
from .models import Booking

RENTAL_DURATION_CHOICES = [
    ("1 Month", "1 Month"),
    ("6 Months", "6 Months"),
    ("1 Year", "1 Year"),
    ("more than 2 years", "more than 2 years"),
]   

class BookingForm(forms.ModelForm):
    move_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    rental_duration = forms.ChoiceField(choices=RENTAL_DURATION_CHOICES)

    class Meta:
        model = Booking
        fields = ['move_in_date', 'rental_duration']
