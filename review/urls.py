""" review URL Configuration


"""
from django.urls import path

import review.views
from review.views import (
    # HomeView,
    TicketDetailView,
    TicketCreateView,
    TicketUpdateView,
    ReviewCreateView,
    UserUnsubscribeView,
    UserSubscriptionsView,
)


urlpatterns = [
    path("", review.views.feed, name="feed"),
    path("feed/", review.views.feed, name="feed"),
    path("home/", review.views.feed, name="home"),
    # path("home/", HomeView.as_view(template_name="review/home.html"), name="home"),
    path(
        "create-ticket/",
        TicketCreateView.as_view(),
        name="create_ticket",
    ),
    path(
        "create-review/",
        ReviewCreateView.as_view(),
        name="create_review",
    ),
    path(
        "<int:pk>/update/",
        TicketUpdateView.as_view(),
        name="update_ticket",
    ),
    path(
        "<int:pk>/view/",
        TicketDetailView.as_view(),
        name="show_ticket",
    ),
    path(
        "subscriptions/",
        UserSubscriptionsView.as_view(),
        name="subscriptions",
    ),
    path(
        "<int:pk>/unsubscribe/",
        UserUnsubscribeView.as_view(),
        name="unsubscribe_user",
    ),
]
