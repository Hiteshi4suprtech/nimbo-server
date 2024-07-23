from django.urls import path
from user_profile.views import create_profile

urlpatterns=[
    path('profiles/', create_profile, name='create_profile'),
    path('add-user/', create_profile, name='create_profile'),
]