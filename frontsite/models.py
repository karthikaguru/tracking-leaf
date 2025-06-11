from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils.crypto import get_random_string
from django.utils import timezone

class CustomUser(AbstractUser):
    
    username = models.CharField(max_length=100, unique=True)  # A unique username for the client
    email = models.EmailField(max_length=255, db_index=True) 
    phone_number = models.CharField(max_length=10, blank=True)  # Client's phone number
    site_location = models.CharField(max_length=255, blank=True)  # Location of the client's site
    site_name = models.CharField(max_length=100, blank=True)  # Site name for identification
    project_start_date = models.DateField(blank=True, null=True)  # Nullable start date for client's project
    project_end_date = models.DateField(blank=True, null=True)  # Nullable end date for the project
    documents = models.FileField(upload_to='client_documents/', blank=True)  # Field to store related documents
    
    def __str__(self):
        return self.username

    # Role-based field using choices
 
    ADMIN = 'ADMIN'
    CLIENT = 'CLIENT'
    TEAM_USER = 'TEAM_USER'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CLIENT, 'Client'),
        (TEAM_USER, 'Team User'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENT)


    # Set related_name for groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Unique related_name
        blank=True
    )

    def __str__(self):
        return self.username
    

    

