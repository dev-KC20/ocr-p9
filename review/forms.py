# from django.contrib.auth import get_user_model
from django.forms import ModelForm
from . import models
from django import forms


class TicketForm(ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]

    title = forms.CharField(label="Titre", label_suffix="")
    description = forms.CharField(max_length=2048, label_suffix="")
    image = forms.ImageField(label_suffix="")


class ReviewForm(ModelForm):
    class Meta:
        model = models.Review
        fields = ["ticket", "rating", "user", "headline", "body"]


class UserFollowsForm(ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ["user", "followed_user"]
