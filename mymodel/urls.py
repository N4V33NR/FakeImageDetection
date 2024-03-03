from django.urls import path
from . import views


urlpatterns=[
    path("",views.welcome, name="welcome"),
    path("home",views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("log_in", views.logIn, name="log_in"),
] 