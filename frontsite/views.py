from django.shortcuts import render,redirect 
from django.contrib.auth.models import User 
from .models import CustomUser
from django.core.paginator import Paginator
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from .forms import LoginForm
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')  # Set the role explicitly as 'client'

        # Additional fields relevant to the client
        phone_number = request.POST.get('phone_number')
        site_location = request.POST.get('site_location')
        site_name = request.POST.get('site_name')
        project_start_date = request.POST.get('project_start_date')
        project_end_date = request.POST.get('project_end_date')

        

        if password1 != password2:
            messages.warning(request, 'The passwords you entered did not match. Please try again.')
            return redirect('register')
    
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already taken. Please choose another one.')
            return redirect('register')

        # Check if email already exists
        

        # Create the user if validations pass
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            phone_number=phone_number,
            site_location=site_location,

            site_name=site_name,
            project_start_date=project_start_date,
            project_end_date=project_end_date
        )
       

     
        send_mail(
            "Welcome to Leaf Construction!",  # Subject of the email
            f"Hi {username},\n\nYou are successfully registered\n\nThank you for registering with Leaf Construction.We are happy to have you on board and look forward to delivering exceptional service.\n\nBest regards,\nThe Leaf Construction Team"
            'dglkarthika97@gmail.com',  # From email
            [email]  # Recipient list
        )

        # Assign the appropriate role
        if role == 'admin':
            user.role = CustomUser.ADMIN
        elif role == 'team_user':
            user.role = CustomUser.TEAM_USER
        elif role == 'client':
            user.role = CustomUser.CLIENT
        else:
            messages.warning(request, 'Invalid role selected. Please try again.')
            return redirect('register')  # Redirect back if role is invalid

        # Save the user with assigned role
        
       
        user.save()

        # Log the user in after successful registration
        login(request, user)
        messages.success(request, 'You have successfully registered. Welcome, {}!'.format(user.username))
        return redirect('/')  # Redirect to a common dashboard or homepage

    # For GET requests, render the registration form
    return render(request, 'frontsite/register.html')


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')

                # Redirect based on the user's role
                if user.role == CustomUser.ADMIN:
                    return redirect('site/admin_dashboard/')
                elif user.role == CustomUser.TEAM_USER:
                    return redirect('site/manage_projects/')
                elif user.role == CustomUser.CLIENT:
                    return redirect('site/projects/add/')
                else:
                    messages.warning(request, 'Invalid user role. Please contact support.')
                    return redirect('index')
            else:
                messages.warning(request, 'Invalid credentials. Please try again.')
                return redirect('login')

    return render(request, 'frontsite/login.html', {'form': form})




def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('/')

def index(request):
     return render(request, 'frontsite/index.html')

def contact_us(request):
      return render(request, 'frontsite/contactus.html')


def about_us(request):
    return render(request, 'frontsite/about.html')  # Ensure the template exists at this location

def client_list(request):
     client =CustomUser.objects.all()
     page=Paginator(client,2)
     page_list =request.GET.get('page')
     page=page.get_page(page_list)
     return render(request, 'frontsite/client/client_list.html',{'clients':page})

def client_update(request,id):
       user =CustomUser.objects.get(id=id)
       if request.method == "POST":
           form = UserRegistrationForm(request.POST,instance=user)
           if form.is_valid():
               form.save()
       return render(request, 'frontsite/client/client_edit.html',{'clients':form})