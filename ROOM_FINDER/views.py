from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from Landlord.models import Landlord, Room
from Renter.models import Renter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def homepage(request):
    room_list = Room.objects.all()
    paginator = Paginator(room_list, 4)  # Show 8 rooms per page

    page = request.GET.get('page', 1)  # Get current page number from URL, default is 1
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)  # If page is not an integer, show first page
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)  # If page is out of range, show last page

    # If on the last page and fewer than 8 rooms remain, ensure it is shown
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

def contact_view(request):
    return render(request, 'contact.html')

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
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('landlord_signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('landlord_signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('landlord_signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Signup successful! Please log in.")
        return redirect('landlord_login')

    return render(request, 'landlord/landlord_signup.html')

def landlord_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Find the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landlord_home')
        else:
            messages.error(request, "Invalid credentials! Please try again.")
            return redirect('landlord_login')

    return render(request, 'landlord/landlord_login.html')


def manage_landlords(request):
    return render(request, "manage_landlords.html")

def manage_renters(request):
    return render(request, "manage_renters.html")

def admin_dashboard(request):
    landlords_list = Landlord.objects.all()
    renters_list = Renter.objects.all()
    rooms = Room.objects.all()
    context = {
        'landlords_list' : landlords_list,
        'renters_list' : renters_list,
        'rooms' : rooms
    }
    return render(request, 'admin_home.html', context)


def renter_signup(request):
    if request.method == 'POST':
        # Collect form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        contact_number = request.POST.get('contact_number')

        # Validate passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('renter_signup')

        # Check if email or username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('renter_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('renter_signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        Renter.objects.create(user=user, contact_number=contact_number)

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

        if user:
            user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('renter_home')
        else:
            messages.error(request, "Invalid credentials! Please try again.")
            return redirect('renter_login')

    return render(request, 'renter/renter_login.html')

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, "room_details.html", {"room": room})


def Logout(request):
    logout(request)
    return redirect('homepage')

