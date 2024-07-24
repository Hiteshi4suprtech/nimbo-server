"""
URL configuration for nimbo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path,include # type: ignore
#from health_goals.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('health_goals.urls')),
    path('api/', include('nimbouser.urls')),
    path('api/', include('feed_post.urls')),
    path('api/', include('user_profile.urls')),
    path('api/', include('user_diagnosis.urls')),
    path('api/', include('user_symptoms.urls')),
]
