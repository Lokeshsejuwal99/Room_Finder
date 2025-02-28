from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from Landlord.models import Landlord, Room
from Renter.models import Renter, Review, Booking
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def homepage(request):
    room_list = Room.objects.filter(is_available=True)

    paginator = Paginator(room_list, 4)

    page = request.GET.get('page', 1)
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)

    if rooms.number == paginator.num_pages and rooms.has_previous():
        next_page = None  # No next page
    else:
        next_page = rooms.next_page_number() if rooms.has_next() else None

    return render(request, 'homepage.html', {'rooms': rooms, 'next_page': next_page})


def login_as_view(request):
    return render(request, 'login_as.html')

def signup_as_view(request):
   return render(request, 'signup_as.html')

def about_view(request):
 return render(request, 'about.html')

def feedback_view(request, room_id=None):
    if room_id:
        # Fetch the room if it's a room-specific review
        room = get_object_or_404(Room, id=room_id)
    else:
        # Otherwise, it's for general feedback, no specific room
        room = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if room:  # Room-specific review
            if request.user.is_authenticated:
                # Ensure only previous renters can leave a review
                if Booking.objects.filter(room=room, renter=request.user.renter).exists():
                    review = Review(name=request.user.username, email=request.user.email, comment=message, room=room, renter=request.user.renter)
                else:
                    return redirect('room_details', room_id=room.id)  # Unauthorized review attempt
            else:
                # If not logged in, prompt user to log in
                return redirect('renter_login')
        else:  # General feedback
            review = Review(name=name, email=email, comment=message, room=None)  # No room for general feedback

        review.save()
        return redirect('feedbacks')  # Redirect to feedbacks page or room detail page

    # For viewing the reviews
    if room:
        reviews = Review.objects.filter(room=room).order_by('-created_on')
        user_has_booked = Booking.objects.filter(room=room, renter=request.user.renter).exists() if request.user.is_authenticated else False
        return render(request, 'room_details.html', {'room': room, 'reviews': reviews, 'user_has_booked': user_has_booked})
    else:
        # For general feedback page
        feedbacks = Review.objects.filter(room__isnull=True).order_by('-created_on')
        return render(request, 'feedback.html', {'feedbacks': feedbacks})
    
    

def admin_feedbacks(request):
    feedbacks = Review.objects.all().order_by('-created_on')    
    return render(request, 'admin_feedbacks.html', {'feedbacks': feedbacks})


def feedback_detail(request, feedback_id):
    feedback = get_object_or_404(Review, pk=feedback_id)
    return render(request, 'feedback_detail.html', {'feedback': feedback})

def admin_login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("admin_home") 
        else:
            error = "yes"
    else:
        error = "no"
    
    return render(request, "admin_login.html", {"error": error})


def landlord_signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        contact_number = request.POST['contact_number']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            print("Passwords do not match!")
            return redirect('landlord_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            print("Email already registered!")
            return redirect('landlord_signup')

        # Create user
        user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
        print(f"User created: {user}")

        landlord = Landlord.objects.create(user=user, contact_number=contact_number, is_landlord=True)
        print(f"Landlord created: {landlord}")

        messages.success(request, "Signup successful! You can now log in.")
        return redirect('landlord_login')

    return render(request, 'landlord/landlord_signup.html')



def landlord_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            print(f"User found: {user}")
        except User.DoesNotExist:
            print("User does not exist!")
            user = None

        if user:
            print(f"User exists and has landlord: {hasattr(user, 'landlord')}")
            if hasattr(user, 'landlord'):
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    print("Authentication successful!")
                    login(request, user)
                    return redirect('landlord_home')
                else:
                    print("Authentication failed!")
            else:
                print("User is not a landlord!")

        messages.error(request, "Invalid credentials or not a landlord!")
        print("Invalid credentials or not a landlord!")
        return redirect('landlord_login')

    return render(request, 'landlord/landlord_login.html')

 
def manage_landlords(request):
    landlord = Landlord.objects.all()
    context = {
        'landlords': landlord,
    }
    return render(request, "manage_landlords.html", context)


def delete_landlord(request, landlord_id):
    if request.method == "POST":
        landlord = get_object_or_404(Landlord, id=landlord_id)
        landlord.delete()
        messages.success(request, "Landlord deleted successfully!")
    return redirect('manage_landlords') 


def manage_renters(request):
    renters = Renter.objects.all()
    context = {
        'renters': renters
    }
    return render(request, "manage_renters.html", context)


def delete_renter(request, renter_id):
    if request.method == "POST":
        renter = get_object_or_404(Renter, id=renter_id)
        renter.delete()
        messages.success(request, "Renter deleted successfully!")
    return redirect('manage_renters') 


def admin_dashboard(request):
    landlords_list = Landlord.objects.all().count()
    renters_list = Renter.objects.all()
    rooms = Room.objects.all().count()
    total_users = User.objects.all().count()
    available_rooms = Room.objects.filter(is_available=True).count()
    recent_bookings = Booking.objects.all().order_by('-booking_date')
    context = {
        'landlords_list' : landlords_list,
        'renters_list' : renters_list,
        'total_rooms' : rooms,
        'active_users' : total_users,
        'available_rooms' : available_rooms,
        'recent_bookings': recent_bookings,
    
    }
    return render(request, 'admin_home.html', context)


def renter_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        contact_number = request.POST['contact_number']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('renter_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('renter_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('renter_signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        Renter.objects.create(user=user, contact_number=contact_number, is_renter=True)

        messages.success(request, "Signup successful! You can now log in.")
        return redirect('renter_login')

    return render(request, 'renter/renter_signup.html')


def renter_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user and hasattr(user, 'renter'):
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('renter_home')

        messages.error(request, "Invalid credentials or not a renter!")
        return redirect('renter_login')

    return render(request, 'renter/renter_login.html')


def room_details(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    reviews = room.reviews.all()  # Fetch all reviews

    return render(request, "room_details.html", {"room": room, "reviews": reviews})


def admin_manage_rooms(request):
    rooms = Room.objects.all()
    return render(request, "admin_manage_rooms.html", {"rooms": rooms})

def all_bookings(request):
    bookings = Booking.objects.all()
    context = {
        "bookings" : bookings,
    }
    return render(request, "all_bookings.html", context)

def Logout(request):
    logout(request)
    return redirect('homepage')

