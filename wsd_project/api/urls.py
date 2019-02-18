from django.urls import path
from . import views
urlpatterns = [
    path('', views.RESTapi, name='RESTapi'),
]