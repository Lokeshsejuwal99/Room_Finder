from django import forms
from .models import Room, RoomImage

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['title', 'price', 'location', 'description', 'room_type']


class RoomImageForm(forms.ModelForm):
    class Meta:
        model = RoomImage
        fields = ['image']