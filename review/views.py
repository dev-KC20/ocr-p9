from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import CharField, Value, Q  # , F

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy  # reverse,

from django.views.generic import DetailView, ListView  # TemplateView,
from django.views.generic.edit import CreateView, DeleteView, UpdateView  # , FormView

from review.forms import TicketForm, UserSubscriptionsForm, ReviewCreateForm
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
    # make a django join==select_related to get the R + T details for followees or myself
    reviews = Review.objects.select_related("ticket").filter(
        Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user")) | Q(user=request.user)
    )
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    # ticket w/o reviews
    tickets = Ticket.objects.filter(
        Q(user__in=UserFollows.objects.filter(user=request.user).values("followed_user")) | Q(user=request.user)
    ).exclude(id__in=reviews.values("ticket_id"))
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    # print(tickets.query)
    # prepare the mixed posts
    posts = sorted(chain(reviews, tickets), key=lambda post: (post.time_created), reverse=True)
    context = {"posts": posts}
    return render(request, "review/feed.html", context=context)

@login_required()
def posts(request):
    """
    A. get my own T + my own R
        sorting : date,
    when R show T related whatever date
    """
    # make a django join==select_related to get the R + T details for followees or myself
    reviews = Review.objects.select_related("ticket").filter(
        Q(user=request.user)
    )
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    # ticket w/o reviews
    tickets = Ticket.objects.filter(
         Q(user=request.user)
    ).exclude(id__in=reviews.values("ticket_id"))
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    # print(tickets.query)
    # prepare the mixed posts
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
    success_url = "/feed"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewCreateView(CreateView, LoginRequiredMixin):
    model = Review
    form_class = ReviewCreateForm
    template_name = "review/create_review.html"
    success_url = "/feed"
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        if self.kwargs.get("pk"):
            self.related_ticket_id = self.kwargs.get("pk")
        return super(ReviewCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        """manage review then save subcribed user"""

        form = self.form_class(request.POST, self.related_ticket_id)

        if form.is_valid():
            related_ticket = get_object_or_404(Ticket, id=self.related_ticket_id)
            rating = form.cleaned_data.get("rating")
            headline = form.cleaned_data.get("headline")
            body = form.cleaned_data.get("body")
            Review.objects.create(ticket=related_ticket, rating=rating, user=self.user, headline=headline, body=body)
            return redirect("feed")
        context = {
            "form": form,
        }
        return render((request), self.template_name, context=context)


class ReviewCreateFullView(CreateView, LoginRequiredMixin):
    model = Review
    fields = "__all__"
    template_name = "review/create_full_review.html"
    success_url = "/feed"

    def get(self, request):
        """provide the 2 inputs to ticket & review"""
        form_ticket = TicketForm()
        form_review = ReviewCreateForm()

        context = {
            "form_ticket": form_ticket,
            "form_review": form_review,
        }
        return render((request), self.template_name, context=context)

    def post(self, request):
        """manage review then save ticket and review"""

        form_ticket = TicketForm(request.POST, request.FILES)
        form_review = ReviewCreateForm(request.POST)
        # if form_ticket.is_valid() and not(form_review.is_valid()):
        #     title = form_ticket.cleaned_data.get("title")
        #     description = form_ticket.cleaned_data.get("decription")
        #     user = request.user
        #     image = form_ticket.cleaned_data.get("image")
        #     ticket_to_review = Ticket.objects.create(title=title, description=description, user=user, image=image)
        if all([form_ticket.is_valid(), form_review.is_valid()]):
            title = form_ticket.cleaned_data.get("title")
            description = form_ticket.cleaned_data.get("description")
            user = request.user
            image = form_ticket.cleaned_data.get("image")
            ticket_to_review = Ticket.objects.create(title=title, description=description, user=user, image=image)

            rating = form_review.cleaned_data.get("rating")
            headline = form_review.cleaned_data.get("headline")
            body = form_review.cleaned_data.get("body")
            Review.objects.create(ticket=ticket_to_review, rating=rating, user=request.user, headline=headline, body=body)
            return redirect("feed")
        context = {
            "form_ticket": form_ticket,
            "form_review": form_review,
        }
        return render((request), self.template_name, context=context)


class TicketUpdateView(UpdateView, LoginRequiredMixin):
    # needed to initiate the form with the value from the object
    # initial = {}

    model = Ticket
    fields = ["title", "description", "image"]
    # form_class = TicketForm
    template_name = "review/update_ticket.html"
    success_url = "/posts"
    pk_url_kwarg = "pk"

    # def get_initial(self):
    #     self.initial = super().get_initial()
    #     self.initial["title"] = self.object.title
    #     self.initial["description"] = self.object.description
    #     self.initial["image"] = self.object.image
    #     return self.initial
    
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)


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
