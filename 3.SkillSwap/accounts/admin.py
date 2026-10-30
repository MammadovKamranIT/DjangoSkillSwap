from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

# Unregister if already registered somewhere else to avoid conflicts
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User)