
from django.urls import path

from ops.views import GithubWebhookView, SlackOAuthView, slack_events_handler

app_name = 'ops'
urlpatterns = [
    path('github/webhook', GithubWebhookView.as_view(), name='github-webhook'),
    # path('/slack/authorize', redirect_slack_authorize),
    # path('/slack/code', SlackAuthCodeView),
    path('slack/events', slack_events_handler, name='handle'),
    path('slack/install', SlackOAuthView.as_view(), name='install'),
    path('slack/oauth_redirect', SlackOAuthView.as_view(), name='oauth_redirect'),
]
