from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import CharField, Value
# from django.http import HttpResponseRedirect  # HttpResponse,
from django.shortcuts import render
from django.urls import reverse_lazy  # reverse,

# from django.conf import settings
from django.views.generic import DetailView, ListView  # TemplateView,
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from review.forms import TicketForm, UserSubscribeForm
from review.models import Review, Ticket, UserFollows

# class SuccessDeleteMessageMixin:
#     success_message = ""

#     def delete(self, *args, **kwargs):
#         response = super().delete(*args, **kwargs)
#         success_message = self.get_success_message()
#         if success_message:
#             messages.success(self.request, success_message)
#         return response

#     def get_success_message(self):
#         return self.success_message


@login_required()
def feed(request):
    reviews = Review.objects.all()
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    context = {"posts": posts}
    return render(request, "review/feed.html", context=context)


class HomeView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "review/home.html"
    paginate_by = 5


class TicketDetailView(DetailView, LoginRequiredMixin):
    model = Ticket
    template_name = "review/show_ticket.html"


class TicketCreateView(CreateView, LoginRequiredMixin):
    model = Ticket
    form_class = TicketForm
    template_name = "review/create_ticket.html"
    success_url = "/home"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewCreateView(CreateView, LoginRequiredMixin):
    model = Review
    fields = "__all__"
    template_name = "review/create_review.html"
    success_url = "/home"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(UpdateView, LoginRequiredMixin):
    model = Ticket
    form_class = TicketForm
    template_name = "review/update_ticket.html"
    success_url = "/home"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserSubscribeView(CreateView, LoginRequiredMixin):
    model = UserFollows
    form_class = UserSubscribeForm
    template_name = "review/subscribe_user.html"
    success_url = "/home"

    def get_form_kwargs(self):
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""
        kwargs = super(UserSubscribeView, self).get_form_kwargs()
        kwargs["request_user"] = self.request.user
        kwargs["former_followed_user"] = UserFollows.objects.filter(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UserSubscriptionView(LoginRequiredMixin, ListView):
    model = UserFollows
    template_name = "review/subscriptions.html"

    def get_queryset(self):
        return UserFollows.objects.filter(user=self.request.user)


class UserUnsubscribeView(DeleteView, LoginRequiredMixin):
    model = UserFollows
    success_url = reverse_lazy("subscriptions")
    success_message = "L'abonné a été supprimé."
    template_name_suffix = "_confirm_delete"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy("subscriptions")


class UserFollowersView(LoginRequiredMixin, ListView):
    model = UserFollows
    template_name = "review/followers.html"

    def get_queryset(self):
        return UserFollows.objects.filter(followed_user=self.request.user)

