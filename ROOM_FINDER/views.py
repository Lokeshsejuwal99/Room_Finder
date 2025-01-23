from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from Landlord.models import Landlord


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




def landlord_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage') 
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in both fields.')

    return render(request, 'landlord/landlord_login.html')

def landlord_signup(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        contact_number = request.POST['contact_number']
        address = request.POST['address']
        profile_picture = request.FILES.get('profile_picture')

        # Validate user existence
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please try another.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please try another.')
        else:
            # Create user and landlord profile
            user = User.objects.create_user(username=username, email=email, password=password, first_name=full_name)
            Landlord.objects.create(
                user=user,
                contact_number=contact_number,
                address=address,
                profile_picture=profile_picture
            )
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('landlord_login')

    return render(request, 'landlord/landlord_signup.html')


def Renter_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST['email_id']
        pwd = request.POST['password']
        user = authenticate(username=email, password=pwd)
        if user:
            login(request, user)
            return redirect('donor_home')
        else:
            error = "yes"
    return render(request, 'renter/renter_login.html', {'error': error})


def admin_dashboard(request):
    return render(request, 'admin_home.html')

def renter_signup(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email_id']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        district = request.POST.get('district')
        country = request.POST.get('country')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('donor_signup')

        # Additional validation (if needed)
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('donor_signup')

        # Check if the username already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Username already taken.")
            return redirect('donor_signup')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('donor_signup')

        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password, first_name=firstname, last_name=lastname)
        user.save()

        # Create the Donor associated with the user
        # donor = Dnor.objects.create(
        #     user=user,
        #     phone_number=phone_number,
        #     address=address,
        #     district=district,
        #     country=country
        # )
        # donor.save()

        # Log the user in after successful signup
        login(request, user)
        messages.success(request, "Signup successful. You are now logged in.")
        return redirect('donor_login')

    return render(request, 'renter/renter_signup.html')

def Logout(request):
    logout(request)
    return redirect('homepage')
