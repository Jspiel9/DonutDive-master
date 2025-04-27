# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("Home/", views.Home, name="Home"),
    path("Calendar/", views.Calendar, name="Calendar"),
    path("Contacts/", views.Contacts, name="Contacts"),
    path("Login/", views.Login, name="Login"),
    path("checkAuth/", views.check_authentication, name="check_auth"),
    path("Signup/", views.Signup, name="Signup"),
    path("Logout/", views.Logout, name="Logout"),
    path("Activate/<uidb64>/<token>/", views.Activate, name="activate"),
     path("Weekly_reward/", views.Weekly_reward, name="Weekly_reward"),

]
