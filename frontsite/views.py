from django.shortcuts import render,redirect 
from django.contrib.auth.models import User 
from .models import CustomUser
from django.core.paginator import Paginator
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from django.core.mail import send_mail
from projectsite.models import Project,Expense
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from .models import CustomUser
from .forms import UserRegistrationForm
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            username =form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            project_start_date = form.cleaned_data['project_start_date']
            project_end_date = form.cleaned_data['project_end_date']
            if password1 != password2:
                messages.warning(request, 'The passwords you entered did not match. Please try again.')
                return redirect('register')
            
        # Check if username already exists
            if CustomUser.objects.filter(username=username).exists():
                messages.warning(request, 'Username already taken. Please choose another one.')
                return redirect('register')
            user = form.save()  # Create user object but don't save yet
            user.set_password(form.cleaned_data['password1'])  # Hash password
            user.save()
            subject = "Welcome to Leaf Construction!"
            message = f"""
                    <html>
                        <body style="padding:5px;">
                            <p>Hi {username},<br>You are successfully registered.<br>
                            Thank you for registering with Leaf Construction. We are happy to have you on board and look forward to delivering exceptional service.</p>
                            <p>📅 Project Start Date: <strong>{project_start_date}</strong></p>
                            <p>🚀 Project End Date: <strong>{project_end_date}</strong></p>
                            <h3>Best regards,</h3>
                            <h3>The Leaf Construction Team</h3>
                        </body>
                    </html>
                """

            send_mail(
                    subject,
                    'Welcome to Leaf Construction!',
                    'dglkarthika97@gmail.com',
                    ['dglkarthika97@gmail.com'],  # Send email to the registered user
                    fail_silently=False,
                    html_message=message
                )
            messages.success(request, f'Welcome, {user.username}! You have successfully registered.')
            return redirect('/')

    else:
        form = UserRegistrationForm()
    
    return render(request, 'frontsite//client/client_create.html', {'form': form})



def login_view(request):
    form = LoginForm()  # Retain form data
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            
            # Redirect based on user role
            if user.role == CustomUser.ADMIN:
                return redirect('site/admin_dashboard/')
            elif user.role == CustomUser.TEAM_USER:
                return redirect('site/projects/')
            elif user.role == CustomUser.CLIENT:
                if Project.objects.filter(client=user).exists():
                    return redirect('client/dashboard/')
                else:
                    return redirect('site/projects/add/')
            else:
                messages.warning(request, 'Invalid user role. Please contact support.')
        else:
            messages.warning(request, 'Invalid credentials. Please try again.')

    return render(request, 'frontsite/login.html', {'form': form})



def client_list(request):
    # Get 'per_page' from the request, default to 2 if not provided
    per_page = int(request.GET.get('per_page', 2))  # Default to 2 items per page
    
    # Fetch all clients
    clients = CustomUser.objects.all()
    
    # Apply pagination
    paginator = Paginator(clients, per_page)
    page_number = request.GET.get('page', 1)  # Default to page 1
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'frontsite/client/client_list.html', {'clients': page_obj, 'per_page': per_page})



def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return render(request, 'frontsite/logout.html')

def index(request):
     return render(request, 'frontsite/index.html')

def contact_us(request):
      return render(request, 'frontsite/contactus.html')


def about_us(request):
    return render(request, 'frontsite/about.html')  # Ensure the template exists at this location

def clientlist(request):
     client =CustomUser.objects.all()
     page=Paginator(client,2)
     page_list =request.GET.get('page')
     page=page.get_page(page_list)
     return render(request, 'frontsite/client/client_list.html',{'clients':page})
     




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CustomUser
from .forms import UserRegistrationForm


@login_required
def client_update(request, id):
    user = get_object_or_404(CustomUser, id=id)

    if request.method == "POST":
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("client_list")


    else:
        form = UserRegistrationForm(instance=user)

    return render(request, "frontsite/client/client_edit.html", {"form": form,'user':user})


def save_projects(request):
     user =CustomUser.objects.all()
     page =Paginator(user,5)
     page_list =request.GET.get('page')
     page =page.get_page(page_list)

     return render(request, 'frontsite/client/save_projects.html',{'page':page})


@login_required
def client_dashboard_view(request):
    # Get all clients for the logged-in user
    clients = CustomUser.objects.filter(username=request.user.username)

    # Get all projects associated with these clients
    projects = Project.objects.filter(client__in=clients).select_related('client')


    # Get all expenses related to these projects
    expenses = Expense.objects.filter(project__in=projects).select_related('project')
    

   


    # Prepare chart data
    project_names = [project.name for project in projects]
    budgets = [float(project.budget) for project in projects]
   
    # Prepare the context for rendering
    context = {
        'clients': clients,
        'projects': projects,
        'expenses':expenses,
        'project_names': project_names,
        'budgets': budgets,
        # Include total spent in the context
    }

    return render(request, 'frontsite/client/clientdashboard.html', context)
