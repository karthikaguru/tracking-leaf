from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    password1= forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '🔒Enter your password',
            'id':'password1',
            'autocomplete': 'off'  # Prevents autofill for email,
        })
    )
    password2= forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id':'password2',
            'placeholder': '🔒Enter your password',
            'autocomplete': 'off'  # Prevents autofill for email
        })
    )
    ADMIN = 'ADMIN'
    CLIENT = 'CLIENT'
    TEAM_USER = 'TEAM_USER'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CLIENT, 'Client'),
        (TEAM_USER, 'Team User'),
    ]
    phone_number = forms.CharField(max_length=10, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': ' 📞Enter your phone number'}))
    site_location = forms.CharField(max_length=255, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Site location',}))
    site_name = forms.CharField(max_length=100, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': ' Site name',}))
    project_start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))
    project_end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True, initial=CustomUser.CLIENT,widget=forms.Select(attrs={'class':'form-control'}))  # Set initial value

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 
                  'phone_number', 'site_location', 'site_name', 'project_start_date', 'project_end_date']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': ' Enter your name',}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': ' Enter your E-mail',}),
           
          
        }
     

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists.")
        return username
    def clean_phone_number(self):
            
                phone_number = self.cleaned_data.get("phone_number")

                if not phone_number.isdigit():
                    raise forms.ValidationError("Phone number must contain only digits.")

                if len(phone_number) != 10:
                    raise forms.ValidationError("The phone number must be exactly 10 digits.")

                return phone_number 
    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        # Ensure the password meets security criteria
        
        if password1 !=password2 :
               raise forms.ValidationError("Password Missmatch..!")

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off'  # Ensures manual input for username
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'off'  # Prevents autofill for email
        })
    )
