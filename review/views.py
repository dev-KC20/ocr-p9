from django.views.generic import TemplateView
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'review/home.html'

# @login_required
# def follow_users(request):
#     form = forms.FollowUsersForm(instance=request.user)
#     if request.method == 'POST':
#         form = forms.FollowUsersForm(request.POST,  instance=request.user)
#         if form.is_valid():
#             form.save()

#             return redirect(settings.LOGIN_REDIRECT_URL)
#     return render(request, 'authentication/follow_users.html', context={'form': form})
