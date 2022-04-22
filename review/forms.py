# from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from . import models

# from authentication.models import User
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


class UserSubscriptionsForm(ModelForm):
    """
    UI: remove label but use placeholder
    validation: Check the user to subscribe to

    """

    def __init__(self, *args, **kwargs):
        """
        get the connected user from the view.
        the former followed user could have been built locally rather than from view.
        """
        if kwargs:
            self.request_user = kwargs.pop("request_user")
            self.former_followed_user = kwargs.pop("former_followed_user")
        super(UserSubscriptionsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.UserFollows
        fields = ["followed_user"]
        followed_user = forms.CharField(
            label="", widget=forms.TextInput(attrs={"class": "validate", "placeholder": "Nom d’utilisateur"})
        )

    def clean_followed_user(self):
        data = self.cleaned_data["followed_user"]
        if self.request_user:
            if self.request_user == data:
                raise ValidationError("Vous ne pouvez vous suivre vous-même!", code="invalid")
            if self.former_followed_user.filter(followed_user=data).exists():
                raise ValidationError("Abonné déja suivi!", code="invalid")
        return data


class ReviewCreateForm(ModelForm):
    """ """

    # def __init__(self, *args, **kwargs):
    #     """
    #     get the connected user from the view.
    #     the former followed user could have been built locally rather than from view.
    #     """
    #     if "request_user" in kwargs:
    #         self.request_user = kwargs["request_user"]
    #         self.related_ticket = kwargs["related_ticket"]
    #     super(ReviewCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]
