from django.urls import path # type: ignore
from health_goals.views import create_health_goal

urlpatterns=[
    path('add-health-goal/', create_health_goal, name='create_health_goal'),
]