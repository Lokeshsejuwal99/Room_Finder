from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from Landlord.models import Landlord
from Renter.models import Renter


def homepage(request):
    return render(request, 'homepage.html')

def login_as_view(request):
    return render(request, 'login_as.html')

def signup_as_view(request):
   return render(request, 'signup_as.html')

def about_view(request):
 return render(request, 'about.html')


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
            # Authenticate using the username and password
            user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landlord_home')
        else:
            messages.error(request, "Invalid credentials! Please try again.")
            return redirect('landlord_login')

    return render(request, 'landlord/landlord_login.html')

def admin_dashboard(request):
    return render(request, 'admin_home.html')


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

        # Create User and Renter Profile
        user = User.objects.create_user(username=username, email=email, password=password)
        Renter.objects.create(user=user, contact_number=contact_number)

        messages.success(request, "Signup successful! You can now log in.")
        return redirect('renter_login')

    return render(request, 'renter/renter_signup.html')


def renter_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            # Authenticate using the username and password
            user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('renter_home')
        else:
            messages.error(request, "Invalid credentials! Please try again.")
            return redirect('renter_login')

    return render(request, 'renter/renter_login.html')


def Logout(request):
    logout(request)
    return redirect('homepage')
