from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

# from django.forms import ModelForm
from django import forms


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"class": "validate", "placeholder": "Nom d’utilisateur"})
    )
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Mot de Passe"}))


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)

    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"class": "validate", "placeholder": "Nom d’utilisateur"})
    )
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Mot de Passe"}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Confirmer Mot de Passe"}))


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()

    old_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Ancien Mot de Passe"}))
    new_password1 = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "Nouveau Mot de Passe"})
    )
    new_password2 = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "Confirmer Mot de Passe"})
    )


# class FollowUsersForm(ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ['follows']
