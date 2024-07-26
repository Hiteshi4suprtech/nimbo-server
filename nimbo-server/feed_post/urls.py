from django.urls import path # type: ignore
from .views import create_post_feed,create_post

urlpatterns=[
    path('create-post-feed/', create_post_feed, name='create_post_feed'),
    path('create-post/',create_post,name='create_post'),
]