from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Landlord, RoomImage
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, RoomImageForm
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.

@login_required
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
            room = room_form.save()

            for file in files:
                RoomImage.objects.create(room=room, image=file)

            return redirect('landlord_home')
    else:
        room_form = RoomForm()
    return render(request, 'landlord/post_room.html', {'room_form': room_form})



def manage_rooms(request):
    rooms = Room.objects.filter(owner=request.user)
    return render(request, 'manage_rooms.html', {'rooms': rooms})


def delete_room_image(request, image_id):
    image = get_object_or_404(RoomImage, id=image_id)
    room_id = image.room.id
    image.delete()
    return redirect('edit_room', room_id=room_id)



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
