"""litreview URL Configuration

"""
from django.urls import path


# authentication
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
import authentication.views

from authentication.forms import CustomAuthForm, CustomPasswordChangeForm

urlpatterns = [
    path("signup/", authentication.views.signup_page, name="signup"),
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html",
            authentication_form=CustomAuthForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "change-password/",
        PasswordChangeView.as_view(
            template_name="authentication/password_change.html",
            form_class=CustomPasswordChangeForm,
        ),
        name="password_change",
    ),
    path(
        "change-password-done/",
        PasswordChangeDoneView.as_view(template_name="authentication/password_change_done.html"),
        name="password_change_done",
    ),
]
