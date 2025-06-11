from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'role',
        'email',
        'site_location',
        'site_name',
     
       
    )
    search_fields = (
        'username',
        'phone_number',
        'email',
        'site_location',
        'site_name'
    )


# Register the CustomUser model with the customized admin
admin.site.register(CustomUser, CustomUserAdmin)
