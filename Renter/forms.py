from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True
    )

    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']
