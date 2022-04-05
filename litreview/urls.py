"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin

# authentication
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

import authentication.views
import review.views
from review.views import HomeView, TicketDetailView, TicketCreate, TicketUpdate
from authentication.forms import CustomAuthForm, CustomPasswordChangeForm

# media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
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
    path("home", HomeView.as_view(template_name="review/home.html"), name="home"),
    path(
        "review/create-ticket",
        review.views.create_ticket,
        name="create_ticket",
    ),
    path(
        "review/open-ticket",
        TicketCreate.as_view(),
        name="open_ticket",
    ),
    path(
        "review/<int:pk>/update",
        TicketUpdate.as_view(),
        name="update_ticket",
    ),
    path(
        "review/<int:pk>/view",
        TicketDetailView.as_view(),
        name="show_ticket",
    ),
]
# lowtech file storage solution for academic purpose & money wise
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
