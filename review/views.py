from django.conf import settings
from django.views.generic import ListView, DetailView  # TemplateView,
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect  # get_object_or_404
from . import forms

from review.models import Ticket


class HomeView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "review/home.html"
    paginate_by = 5


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "review/show_ticket.html"


@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    context = {
        "ticket_form": ticket_form,
    }
    return render(request, "review/create_ticket.html", context=context)


# @login_required
# def follow_users(request):
#     form = forms.FollowUsersForm(instance=request.user)
#     if request.method == 'POST':
#         form = forms.FollowUsersForm(request.POST,  instance=request.user)
#         if form.is_valid():
#             form.save()

#             return redirect(settings.LOGIN_REDIRECT_URL)
#     return render(request, 'authentication/follow_users.html', context={'form': form})
