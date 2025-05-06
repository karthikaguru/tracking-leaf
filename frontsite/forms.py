from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from .models import CustomUser
class UserRegistrationForm(forms.ModelForm):
     password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'new-password'
        })
    )
     password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password'
        })
    )

     class Meta:
        model = CustomUser
        fields = [
             'username', 'phone_number', 'email', 'site_location',
            'site_name', 'project_start_date', 'project_end_date', 'documents'
        ]
        widgets = {
   
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name', 'autocomplete': 'off'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email', 'autocomplete': 'off'}),
            'site_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the site location', 'autocomplete': 'off'}),
            'site_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the site name', 'autocomplete': 'off'}),
            'project_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'autocomplete': 'off'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'autocomplete': 'off'}),
            
          
        }
     def clean_phone_number(self):
            
                phone_number = self.cleaned_data.get("phone_number")

                if not phone_number.isdigit():
                    raise forms.ValidationError("Phone number must contain only digits.")

                if len(phone_number) != 10:
                    raise forms.ValidationError("The phone number must be exactly 10 digits.")

                return phone_number

     
   
      



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
