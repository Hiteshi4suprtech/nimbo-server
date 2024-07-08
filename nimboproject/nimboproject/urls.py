# myproject/urls.py

from django.contrib import admin
from django.urls import path,include 
from nimboapp.views import GraphQLView, csrf_token_view
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
 #   path('api/nimboql/', GraphQLView.as_view(), name='graphql'),
    path('csrf_token/', csrf_token_view, name='csrf_token'),
  #  path('', include('nimboapp.urls')),
    path('', lambda request: redirect('/admin/login/', permanent=True)),
    path('', include('nimboapp.urls')),


]
