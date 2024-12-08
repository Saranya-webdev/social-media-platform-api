from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username',  'profile_picture', 'bio')

    def profile_picture(self, obj):
        return obj.profile.profile_picture.url if obj.profile.profile_picture else "No picture"

    def bio(self, obj):
        return obj.profile.bio[:50]  # Display the first 50 characters of the bio    

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
