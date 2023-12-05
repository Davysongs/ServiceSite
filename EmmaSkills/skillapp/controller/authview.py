from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from skillapp.models import Profile
from skillapp.form import PasswordResetForm

# Function for creating of user account
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpass = request.POST['cpass']

        if password == cpass:
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username not available')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, email=email, password=password)
                user.save()

                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model, user_id = user_model.id, email = email)
                new_profile.save()
                messages.info(request, 'Account created successfully')
                return redirect('login')
        else:
            messages.info(request, "Passwords don't match")
            return redirect('login')
    return render(request, "register.html")

# Function for Logining user account
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password, is_superuser = False)

        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return redirect('/a/dashboard')  # Redirect superusers to the admin dashboard
            else:
                # Redirect regular users to their profile or another appropriate page
                return redirect('/u/dashboard')  # You should change 'profile' to the actual URL name for the user profile page.
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def password_reset(request):
    form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form' : form})

# def recover_password(request):
#     return render(request, 'recover-password.html')