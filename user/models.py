from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user =models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    username =models.CharField(max_length=200,null=True)
    location =models.CharField(max_length=200,null=True)
    phone_number =models.IntegerField(null=True)
    image = models.ImageField( upload_to='profile_pics')
 
    def __str__(self):
        return f'{self.user.username} Profile'
    

