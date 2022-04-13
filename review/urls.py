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

import review.views
from review.views import (
    HomeView,
    TicketDetailView,
    TicketCreateView,
    TicketUpdateView,
    ReviewCreateView,
    UserSubscribeView,
    UserSubscriptionView,
    UserUnsubscribeView,
    UserFollowersView,
    UserSubscriptionsView,
)


urlpatterns = [
    path("review/feed/", review.views.feed, name="feed"),
    path("home/", HomeView.as_view(template_name="review/home.html"), name="home"),
    path(
        "review/create-ticket/",
        TicketCreateView.as_view(),
        name="create_ticket",
    ),
    path(
        "review/create-review/",
        ReviewCreateView.as_view(),
        name="create_review",
    ),
    path(
        "review/<int:pk>/update/",
        TicketUpdateView.as_view(),
        name="update_ticket",
    ),
    path(
        "review/<int:pk>/view/",
        TicketDetailView.as_view(),
        name="show_ticket",
    ),
    path(
        "review/subscribe/",
        UserSubscribeView.as_view(),
        name="subscribe_user",
    ),
    path(
        "review/subscription/",
        UserSubscriptionView.as_view(),
        name="subscription",
    ),
    path(
        "review/subscriptions/",
        UserSubscriptionsView.as_view(),
        name="subscriptions",
    ),
    path(
        "review/<int:pk>/unsubscribe/",
        UserUnsubscribeView.as_view(),
        name="unsubscribe_user",
    ),
    path(
        "review/followers/",
        UserFollowersView.as_view(),
        name="followers",
    ),
]
