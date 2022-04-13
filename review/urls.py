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
    UserSubscribeView,
    UserSubscriptionView,
    UserUnsubscribeView,
    UserFollowersView,
    UserSubscriptionsView,
)


urlpatterns = [
    path("", review.views.feed, name="feed"),
    path("review/feed/", review.views.feed, name="feed"),
    path("review/home/", review.views.feed, name="home"),
    # path("home/", HomeView.as_view(template_name="review/home.html"), name="home"),
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
