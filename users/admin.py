"""
Django admin configuration for users app.

Customizations for the default User model in the admin interface.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Customize the default User admin if needed
# This is optional since Django provides a good default UserAdmin

# Example of customizing the User admin:
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
