from django.shortcuts import render, redirect, get_object_or_404
from .models import Renter, Booking, Room
from django.contrib.auth.decorators import login_required
from .forms import BookingForm

# Create your views here.

@login_required
def renter_home(request):
 available_rooms = Room.objects.filter(is_available=True)
 my_bookings = Booking.objects.filter(renter=request.user.renter)
 
 context = {
        'available_rooms': available_rooms,
        'my_bookings': my_bookings
    }
 return render(request, 'renter/renter_home.html', context)



@login_required
def renter_dashboard(request):
    rooms = Room.objects.all()

    context = {
        'rooms': rooms
    }
    return render(request, 'renter/renter_home.html', context)


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    renter_profile = request.user.renter_profile

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.renter = renter_profile
            booking.save()
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'book_room.html', {'room': room, 'form': form})
   
@login_required
def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    context = {
        'booking': booking
    }
    return render(request, 'booking_confirmation.html', context)
   
   
def available_rooms(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'renter/renter_home.html', {'rooms': rooms})
   
   

@login_required
def cancel_booking(request, booking_id):
    """
    Handles booking cancellation.
    """
    booking = get_object_or_404(Booking, id=booking_id, renter=request.user.renter)
    booking.delete()
    return redirect('renter_home')