from django.urls import path
from . import views  # Import the views module from the current folder

urlpatterns = [
    path('hello/', views.say_hello),
]