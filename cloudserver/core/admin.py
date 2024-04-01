from .models import Game
from .models import GameUser
from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'coming_soon')  # Add 'id' here

admin.site.register(Game, GameAdmin)

class GameUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'game')  # Customize as needed
    search_fields = ('user__username', 'game__name', 'vm_username')  # Enable search functionality
    list_filter = ('game',)  # Filter options
    
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "name_tag")  # Customize this with the fields you want in the creation form

class UserAdmin(BaseUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    list_display = ('username', 'email', 'name_tag', 'is_staff')  # Customize as per your User model
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'name_tag')}),  # Include your custom fields here
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name_tag', 'password1', 'password2'),  # Customize this as well
        }),
    )
    search_fields = ('username', 'name_tag', 'email')
    ordering = ('username',)   
    
admin.site.register(GameUser, GameUserAdmin)
admin.site.register(User, UserAdmin)
