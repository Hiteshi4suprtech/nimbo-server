from django.contrib import admin

# Register your models here.
# nimboapp/admin.py

from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Nimbo Admin'
    site_title = 'Nimbo Admin Portal'
    index_title = 'Welcome to Nimbo Admin'

admin_site = MyAdminSite(name='myadmin')

# Register your models with the custom admin site
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
admin_site.register(User, UserAdmin)
