from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin list view
    list_display = ('username', 'email', 'phone_number', 'is_active', 'is_staff', 'date_joined')
    
    # Define the fields to be used in the admin detail view
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('phone_number', 'profile_picture', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'zip_code')}),
        ('Location Info', {'fields': ('region_name', 'lat', 'lon', 'timezone', 'isp')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    # Define the fields to be used in the admin add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
    # Enable search functionality
    search_fields = ('username', 'email', 'phone_number', 'city', 'state', 'country')
    
    # Enable filtering
    list_filter = ('is_active', 'is_staff', 'date_joined', 'country', 'state')
    
    # Set the ordering of the list view
    ordering = ('-date_joined',)

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)