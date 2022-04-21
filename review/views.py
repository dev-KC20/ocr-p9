from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import CharField, Value, Q  # , F

from django.shortcuts import render, redirect
from django.urls import reverse_lazy  # reverse,

from django.views.generic import DetailView, ListView  # TemplateView,
from django.views.generic.edit import CreateView, DeleteView, UpdateView  # , FormView

from review.forms import TicketForm, UserSubscriptionsForm
from review.models import Review, Ticket, UserFollows


@login_required()
def feed(request):
    """
    A. get my own T + my own R
    B. get my followee T+R
    C. get any R on one of my T -> with a T take all its R

    sorting : date, 
    when R show T related whatever date
    """
    tickets = Ticket.objects.filter(
        Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user")) | Q(user=request.user)
    )
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    # make a django join to get the T details.
    reviews = Review.objects.select_related("ticket").filter(
        Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user")) | Q(user=request.user)
    )
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    # what about sorting R by T#
    # tickets = tickets.annotate(sort_id=F("pk"))
    # reviews = reviews.annotate(sort_id=F("ticket_id"))
    # merge them all in one
    posts = sorted(chain(reviews, tickets), key=lambda post: (post.time_created), reverse=True)

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


class UserSubscriptionsView(LoginRequiredMixin, CreateView):
    model = UserFollows
    form_class = UserSubscriptionsForm
    template_name = "review/subscriptions.html"
    success_url = reverse_lazy("subscriptions")

    def get(self, request):
        """provide the 2 inputs to followers & subscription"""
        subscription_list = UserFollows.objects.filter(user=self.request.user)
        follower_list = UserFollows.objects.filter(followed_user=self.request.user)

        form = self.form_class(request_user=self.request.user, former_followed_user=subscription_list)

        context = {
            "form": form,
            "form_follower": follower_list,
            "form_subscription": subscription_list,
        }
        return render((request), self.template_name, context=context)

    def post(self, request):
        """manage post then save subcribed user"""
        subscription_list = UserFollows.objects.filter(user=self.request.user)
        follower_list = UserFollows.objects.filter(followed_user=self.request.user)
        form = self.form_class(request.POST, request_user=self.request.user, former_followed_user=subscription_list)
        if form.is_valid():
            subscribed_user = form.cleaned_data.get("followed_user")
            current_user = self.request.user
            UserFollows.objects.create(user=current_user, followed_user=subscribed_user)
            return redirect("subscriptions")
        context = {
            "form": form,
            "form_follower": follower_list,
            "form_subscription": subscription_list,
        }
        return render((request), self.template_name, context=context)
