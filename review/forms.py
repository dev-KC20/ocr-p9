# from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from . import models

# from authentication.models import User
from django import forms


class TicketForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """
        get the connected user from the view.
        the former followed user could have been built locally rather than from view.
        """
        super(TicketForm, self).__init__(*args, **kwargs)
        if kwargs:
            if kwargs["instance"]:
                self.fields["title"] = kwargs["instance"].title
                self.fields["description"] = kwargs["instance"].description

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]

    title = forms.CharField(label="Titre", label_suffix="")
    description = forms.CharField(max_length=2048, label_suffix="")
    image = forms.ImageField(label_suffix="")


class ReviewForm(ModelForm):
    # not yet used, to cancel?
    RATINGS = [("1", "*"), ("2", "**"), ("3", "***"), ("4", "****"), ("5", "*****")]

    class Meta:
        model = models.Review
        fields = ["ticket", "rating", "user", "headline", "body"]

    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=RATINGS)


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
    RATINGS = [("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]

    rating = forms.ChoiceField(label="Note", widget=forms.RadioSelect, choices=RATINGS)
    headline = forms.CharField(max_length=128, label="Titre")
    body = forms.CharField(max_length=8192, label="Commentaire")
