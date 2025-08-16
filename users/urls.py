from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from users.forms import CustomSetPasswordForm

app_name = 'users'

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/registration/password_reset_form.html',
        email_template_name='users/registration/password_reset_email.html',
    ), name='password_reset'),
    path(
    'password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        form_class=CustomSetPasswordForm
    ),
    name='password_reset_confirm'
),
]