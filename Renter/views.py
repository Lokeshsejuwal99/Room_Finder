from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Renter, Booking, Room, Review
from Landlord.models import Payment
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from datetime import datetime
from .decorators import renter_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
import json
from decimal import Decimal
import base64
from time import timezone
import uuid
from urllib.parse import urlencode


@login_required
@renter_required
def renter_home(request):
 available_rooms = Room.objects.filter(is_available=True)
 my_bookings = Booking.objects.filter(renter=request.user.renter)
 
 context = {
        'available_rooms': available_rooms,
        'my_bookings': my_bookings
    }
 return render(request, 'renter/renter_home.html', context)


# @login_required
# def book_room(request, room_id):
#     room = get_object_or_404(Room, id=room_id)
    
#     try:
#         renter_profile = request.user.renter
#     except Renter.DoesNotExist:
#         return redirect('some_error_page')

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.room = room
#             booking.renter = renter_profile
#             booking.save()
            
#             print(f"Booking_id: {booking.id}")
#             if booking.id:
#                 return redirect('booking_confirmation', booking_id=booking.id)
#             else:
#                 print("Booking ID is not available!")

#         else:
#             print(form.errors)
#     else:
#         form = BookingForm()

#     return render(request, 'renter/book_now.html', {'room': room, 'form': form})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    context = {
        'booking': booking
    }
    return render(request, 'renter/booking_confirmation.html', context)

   
def available_rooms(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'renter/renter_home.html', {'rooms': rooms})
   

def renter_profile(request):
    renter = request.user.renter
    context = {
        'renter': renter,
        'year': datetime.now().year,
        }
    return render(request, "renter/rent_profile.html", context)


def view_bookings(request):
    bookings = Booking.objects.filter(approved=False)   
    context = {
        'bookings' : bookings,
    }
    
    return render(request, "renter/view_bookings.html", context)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.room.is_available = True
    booking.room.save()

    booking.delete()
    
    messages.success(request, "Your booking has been canceled. The room is now available again.")
    return redirect("view_rooms")

@login_required
def view_rooms(request):
    bookings = Booking.objects.filter(renter=request.user.renter).exclude(status='Rejected').select_related("room")

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        review_content = request.POST.get("review_content")

        booking = get_object_or_404(Booking, id=booking_id, renter=request.user.renter)

        review, created = Review.objects.get_or_create(
            room=booking.room,
            renter=request.user.renter,
            defaults={
                "comment": review_content,
                "name": request.user.renter.user.username,
                "email": request.user.email,
            },
        )
        for booking in bookings:
         print(f"Booking ID: {booking.id}, Room ID: {booking.room.id if booking.room else 'No Room'}")
         
        for booking in Booking.objects.all():
            print(f"Booking ID: {booking.id}, Room: {booking.room}")

        if not created:
            review.comment = review_content
            review.save()

        return JsonResponse({"success": True})

    return render(request, "renter/view_rooms.html", {"bookings": bookings})
    

def submit_review(request, room_id):
    """Handles renter review submission"""
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        review_text = request.POST.get("review_content")

        if review_text:
            Review.objects.create(
                renter=request.user.renter,
                room=room,
                comment=review_text
            )
        return redirect(request.META.get('HTTP_REFERER', 'view_room'))

    return JsonResponse({"success": False})



def book_room(request, id):
    if request.method == 'GET':  # ✅ Allow GET requests
        return render(request, 'renter/book_now.html', {'room_id': id})  # Render form

    elif request.method == 'POST':  # ✅ Handle form submission
        amount = request.POST.get('amount')
        room_id = request.POST.get('room_id')

        if not room_id:
            return HttpResponseBadRequest("Room ID is required.")

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        transaction_id = str(uuid.uuid4())
        merchant_code = 'EPAYTEST'

        context = {
            'amount': amount,
            'merchant_code': merchant_code,
            'product_id': room_id,
            'transaction_id': transaction_id,
            'success_url': 'http://127.0.0.1:8000/success/',
            'failure_url': 'http://127.0.0.1:8000/failure/',
            'name': name,
            'email': email,
            'phone': phone
        }

        return render(request, 'renter/book_now.html', context)

    return HttpResponse("Invalid request method.", status=405)
    
def payment_success(request, name, email, room_id, phone, move_in_date, rental_duration):
    encoded_str = request.GET.get('data')

    if not encoded_str:
        return HttpResponseBadRequest("Missing payment data")

    try:
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')
        decoded_json = json.loads(decoded_str)

        amount = decoded_json.get('total_amount', '0').replace(',', '')  # Clean amount
        transaction_id = decoded_json.get("transaction_uuid")
        payment_amount = Decimal(amount)

    except (json.JSONDecodeError, base64.binascii.Error, Decimal.InvalidOperation) as e:
        return HttpResponseBadRequest(f"Error decoding or converting payment data: {e}")

    if not room_id:
        return HttpResponseBadRequest("Room ID is missing in the response.")

    room = get_object_or_404(Room, id=room_id)
    room.total_booked_amount += payment_amount
    room.save()

    renter = get_object_or_404(Renter, user__email=email)
    renter.save()

    # Save booking details
    Booking.objects.create(
        room=room,
        renter=renter,
        move_in_date=move_in_date,
        rental_duration=rental_duration,
        status="success",
        payment_amount=payment_amount,
        payment_status=True,
    )

    context = {
        'ref_id': transaction_id,
        'amount': payment_amount,
        'room': room,
        'renter': renter,
        'phone': phone,
        'move_in_date': move_in_date,
        'rental_duration': rental_duration, 
    }

    return render(request, 'renter/payment_success.html', context)



def payment_failure(request):
    return render(request, 'renter/payment_failure.html')
