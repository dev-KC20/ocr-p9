""" review URL Configuration


"""
from django.urls import path

import review.views
from review.views import (
    TicketDetailView,
    TicketCreateView,
    TicketUpdateView,
    TicketDeleteView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
    ReviewCreateFullView,
    UserUnsubscribeView,
    UserSubscriptionsView,
)


urlpatterns = [
    path("", review.views.feed, name="feed"),
    path("feed/", review.views.feed, name="feed"),
    path("posts/", review.views.posts, name="posts"),
    path(
        "ticket/create-ticket/",
        TicketCreateView.as_view(),
        name="create_ticket",
    ),
    path(
        "ticket/<int:pk>/update/",
        TicketUpdateView.as_view(),
        name="ticket_update",
    ),
    path(
        "ticket/<int:pk>/delete/",
        TicketDeleteView.as_view(),
        name="ticket_delete",
    ),
    path(
        "ticket/<int:pk>/view/",
        TicketDetailView.as_view(),
        name="ticket_show",
    ),
    path(
        "review/<int:pk>/create-review/",
        ReviewCreateView.as_view(),
        name="review_create",
    ),
    path(
        "review/create-full-review/",
        ReviewCreateFullView.as_view(),
        name="create_full_review",
    ),
    path(
        "review/<int:pk>/update/",
        ReviewUpdateView.as_view(),
        name="review_update",
    ),
    path(
        "review/<int:pk>/delete/",
        ReviewDeleteView.as_view(),
        name="review_delete",
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
