from django.urls import include, path
from . import views

app_name = 'users'

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
]