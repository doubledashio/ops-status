from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        redirect_uri = self.request.build_absolute_uri(reverse('ops:oauth_redirect'))

        # Slack requires a SSL address.
        # even under SSL ngrok, request.build_absolute_uri() builds with HTTP. address this here
        if settings.DEBUG:
            redirect_uri=redirect_uri.replace('http://', 'https://', 1)

        context.update({
            'scope': settings.SLACK_SCOPES,
            'client_id': settings.SLACK_CLIENT_ID,
            'redirect_uri': redirect_uri
            # TODO - optional but more secure: Add `state` - any value unique to the user/session
        })
        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    fields = ['username']
    model = get_user_model()
    success_url = '/accounts/profile'
    template_name = 'accounts/profile.html'

    def get_object(self):
        return self.request.user
