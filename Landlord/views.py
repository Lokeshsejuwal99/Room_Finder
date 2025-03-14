from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, RoomImage, Landlord
from django.contrib.auth.decorators import login_required
from .forms import RoomForm
from django.contrib import messages
from django.http import JsonResponse
from Renter.models import Booking
from .decorators import landlord_required


@login_required
@landlord_required
def landlord_home(request):
 return render(request, 'landlord/landlord_home.html')
 
 
@login_required
def landlord_profile(request):
    landlord = request.user
    context = {
        'landlord': landlord,
    }
    return render(request, 'landlord/land_profile.html', context)


def post_room(request):
    if request.method == "POST":
        room_form = RoomForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')

        if room_form.is_valid():
            room = room_form.save(commit=False)
            room.owner = request.user
            room.save()

            for file in files:
                RoomImage.objects.create(room=room, image=file)

            return redirect('manage_rooms')
    else:
        room_form = RoomForm()

    return render(request, 'landlord/post_room.html', {'room_form': room_form})


def manage_rooms(request):
    landlord = get_object_or_404(Landlord, user=request.user)
    rooms = Room.objects.filter(owner=landlord)
    return render(request, 'manage_rooms.html', {'rooms': rooms})


def delete_room(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(Room, id=room_id)
        
        room_images = RoomImage.objects.filter(room=room)
        room_images.delete()
        
        room.delete()

    return redirect('manage_rooms')




def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    form = RoomForm(instance=room)
    images = RoomImage.objects.filter(room=room)

    if request.method == "POST" and "title" in request.POST:
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("manage_rooms")

    return render(request, "landlord/edit_room.html", {"room": room, "form": form, "images": images})


def upload_room_image(request, room_id):
    if request.method == "POST":
        room = get_object_or_404(Room, id=room_id)
        for file in request.FILES.getlist("images"):
            RoomImage.objects.create(room=room, image=file)

        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)



@login_required
def view_applications(request):
    try:
        landlord = Landlord.objects.get(user=request.user)
        rooms = Room.objects.filter(owner=landlord)
        bookings = Booking.objects.filter(room__in=rooms)
        return render(request, 'landlord/view_applications.html', {'bookings': bookings})
    except Landlord.DoesNotExist:
        return render(request, 'landlord/error.html', {'message': "Landlord not found."})


def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.approved = True
    booking.save()

    room = booking.room
    room.is_available = False
    room.save()
    return redirect('view_applications')  



def reject_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.approved = False
        booking.save()
        return redirect('view_applications')
    return redirect('view_applications')
