from django.conf import settings
from django.contrib.auth import login  # authenticate
from django.shortcuts import redirect, render
# from django.contrib.auth.decorators import login_required

from . import forms


def signup_page(request):
    # train with one FBV
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})


# @login_required
# def follow_users(request):
#     form = forms.FollowUsersForm(instance=request.user)
#     if request.method == 'POST':
#         form = forms.FollowUsersForm(request.POST,  instance=request.user)
#         if form.is_valid():
#             form.save()

#             return redirect(settings.LOGIN_REDIRECT_URL)
#     return render(request, 'authentication/follow_users.html', context={'form': form})
