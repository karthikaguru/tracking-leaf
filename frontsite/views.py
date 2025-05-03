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
       
        # Send email after project is created
        subject = "Welcome to Leaf Construction!"
        message = f"""
            <html>
                <body style="padding:5px;">
                    <p>Hi {username},<br>You are successfully registered<br>Thank you for registering with Leaf Construction.We are happy to have you on board and look forward to delivering exceptional service.</p>
  
                    <p>📅Project  Start Date: <strong>{project_start_date}</strong></p>
                    <p>🚀Project End Date: <strong>{project_end_date}</strong></p>
                   
                    <h3>Best regards
                    <h3>The Leaf Construction Team</h3>
                </body>
            </html>
        """

        send_mail(
            subject,
            'Welcome to Leaf Construction!',
            'dglkarthika97@gmail.com',  # Sender email
            ['dglkarthika97@gmail.com'],  # Recipient email
            fail_silently=False,
            html_message=message  # HTML-formatted email
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

                user = request.user  # Get current user

             
                if user.role == CustomUser.ADMIN:
                    return redirect('site/admin_dashboard/')
                elif user.role == CustomUser.TEAM_USER:
                    return redirect('site/projects/')
                elif user.role == CustomUser.CLIENT:
                       if Project.objects.filter(client=user).exists():  
                                return redirect('site/projects/')  # Redirect to project list
                       else:
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
                if user.project_end_date and user.project_end_date < timezone.now().date():
                    subject = "Update Your Project Deadline!"
                    update_link = f"http://127.0.0.1:8000/update-deadline/{user.id}/"

                    message = f"""
                        <html>
                            <body style="padding:2px;">
                                <p>Dear {request.user.username},</p>
                                <p>Your project <strong>{user.name}</strong> is overdue! Please <a href="{update_link}">click here</a> to update your deadline.</p>
                                <p>Best regards,<br>The Leaf Construction Team</p>
                            </body>
                        </html>
                    """

                    send_mail(
                        subject,
                        "Your project deadline has passed. Click the link to update it.",
                        'dglkarthika97@gmail.com',
                        [request.user.email],  # Send to project owner
                        fail_silently=False,
                        html_message=message
                    )


       return render(request, 'frontsite/client/client_edit.html',{'clients':form})

def save_projects(request):
     user =CustomUser.objects.all()
     page =Paginator(user,4)
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
