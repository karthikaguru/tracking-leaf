from django import forms
from .models import Profile
from frontsite.models  import CustomUser


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
 
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location','phone_number','image']
        widgets = { 
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
