from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView


class HomeView(TemplateView):
    template_name = 'home.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    fields = ['username']
    model = get_user_model()
    success_url = '/accounts/profile'
    template_name = 'accounts/profile.html'

    def get_object(self):
        return self.request.user
