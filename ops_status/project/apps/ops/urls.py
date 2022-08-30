
from django.urls import path

from ops.views import GithubWebhookView, slack_events_handler, slack_oauth_handler

app_name = 'ops'
urlpatterns = [
    path('github/webhook', GithubWebhookView.as_view(), name='github-webhook'),
    # path('/slack/authorize', redirect_slack_authorize),
    # path('/slack/code', SlackAuthCodeView),
    path('slack/events', slack_events_handler, name='handle'),
    path('slack/install', slack_oauth_handler, name='install'),
    path('slack/oauth_redirect', slack_oauth_handler, name='oauth_redirect'),
    # path('slack/install', SlackOAuthView.as_view(), name='install'),
    # path('slack/oauth_redirect', SlackOAuthView.as_view(), name='oauth_redirect'),
]
