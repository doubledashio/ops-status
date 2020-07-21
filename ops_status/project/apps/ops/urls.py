
from django.urls import path

from .views import GithubWebhookView, SlackAuthCodeView, redirect_slack_authorize

app_name = 'ops'
urlpatterns = [
    path('github/webhook', GithubWebhookView.as_view(), name='github-webhook'),
    path('/slack/authorize', redirect_slack_authorize),
    path('/slack/code', SlackAuthCodeView),
]
