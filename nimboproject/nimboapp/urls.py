# nimboapp/urls.py

from django.urls import path
from .schema import schema
# from ariadne.contrib.django.views import GraphQLView
from nimboapp.views import GraphQLView, csrf_token_view




urlpatterns = [
  #  path("graphql/", GraphQLView.as_view(schema=schema), name="graphql"),
      path('api/nimboql/', GraphQLView.as_view(), name='nimboql'),


]
