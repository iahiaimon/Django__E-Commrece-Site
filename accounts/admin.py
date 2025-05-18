from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'phone', 'is_staff']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone', 'address' , 'image')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2', 'phone', 'address' , 'image')}),
    )
    search_fields = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
