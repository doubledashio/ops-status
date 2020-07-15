
from django.urls import path

from .views import GithubWebhookView

app_name = 'ops'
urlpatterns = [
    path('github/webhook', GithubWebhookView.as_view(), name='github-webhook'),
]
