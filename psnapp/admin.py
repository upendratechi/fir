# psnapp/admin.py
from django.contrib import admin
from .models import PSNEntry

# Register the PSNEntry model with the Django admin interface
admin.site.register(PSNEntry)
