from django.urls import path # type: ignore
from nimbouser.views import request_otp, verify_otp, create_user

urlpatterns=[
    path('request-otp/', request_otp, name='request_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),  
    path('create-user/', create_user, name='create_user'),   
]