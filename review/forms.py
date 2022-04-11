# from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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


class UserSubscribeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """Grants access to the request object so that only members of the current user
        are given as options"""
        self.request_user = kwargs.pop("request_user")
        self.former_followed_user = kwargs.pop("former_followed_user")
        super(UserSubscribeForm, self).__init__(*args, **kwargs)
        # self.former_followed_user.queryset = models.UserFollows.objects.filter(user=self.request_user)

    class Meta:
        model = models.UserFollows
        fields = ["followed_user"]
        followed_user = forms.CharField(
            label="", widget=forms.TextInput(attrs={"class": "validate", "placeholder": "Nom d’utilisateur"})
        )

    def clean_followed_user(self):
        data = self.cleaned_data["followed_user"]

        if self.request_user == data:
            raise ValidationError("Vous ne pouvez vous suivre vous-même!", code="invalid")
        if self.former_followed_user.filter(followed_user=data).exists():
            raise ValidationError("Abonné déja suivi!", code="invalid")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data


""" Multiform extras
"""


class MultipleForm(ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ["user", "followed_user"]
        followed_user = forms.CharField(
            label="", widget=forms.TextInput(attrs={"class": "validate", "placeholder": "Nom d’utilisateur"})
        )

    action = forms.CharField(max_length=60, widget=forms.HiddenInput())


class SubscribeForm(MultipleForm):
    """All model attributs are inherited"""

    def __init__(self, *args, **kwargs):
        """Grants access to the request object so that only members of the current user
        are given as options"""
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.request_user = kwargs["initial"].pop("request_user")
        self.former_followed_user = kwargs["initial"].pop("former_followed_user")

    class Meta(MultipleForm.Meta):
        fields = ["followed_user"]

    def clean_followed_user(self):
        data = self.cleaned_data["followed_user"]
        if self.request_user == data:
            raise ValidationError("Vous ne pouvez vous suivre vous-même!", code="invalid")
        if self.former_followed_user.filter(followed_user=data).exists():
            raise ValidationError("Abonné déja suivi!", code="invalid")
        return data


class SubscriptionForm(MultipleForm):
    """All model attributs are inherited"""

    def __init__(self, *args, **kwargs):
        """Grants access to the request object so that only members of the current user
        are given as options"""
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.request_user = kwargs["initial"].pop("request_user")
        self.former_followed_user = kwargs["initial"].pop("former_followed_user")


class FollowerForm(MultipleForm):
    """All model attributs are inherited"""

    def __init__(self, *args, **kwargs):
        """Grants access to the request object so that only members of the current user
        are given as options"""
        super(FollowerForm, self).__init__(*args, **kwargs)
        self.request_user = kwargs["initial"].pop("request_user")
        self.former_following_user = kwargs["initial"].pop("former_following_user")
