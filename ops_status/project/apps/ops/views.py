import json
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.urls import resolve, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from ops.models import SlackBotChannel
from ops.slack import app
import requests
from slack_bolt.adapter.django import SlackRequestHandler
from slack_sdk.web import WebClient

handler = SlackRequestHandler(app=app)

@method_decorator(csrf_exempt, name='dispatch')
class GithubWebhookView(View):
    def _process_incident(self, data):
        incident = data['incident']
        created_at = datetime.fromisoformat(incident['created_at'].replace("Z", "+00:00"))
        impact = incident['impact']
        status = incident['status']
        latest_update = incident['incident_updates'][0]
        latest_update_body = latest_update['body']
        latest_update_created_at = datetime.fromisoformat(latest_update['created_at'].replace("Z", "+00:00"))
        latest_update_status = latest_update['status']

        color = '#CCCCCC'
        if impact == 'minor':
            color = '#FFA500'
        elif impact == 'major':
            color = '#D80000'

        if status == 'resolved':
            color = '#004E00'

        max_time = created_at + timedelta(minutes=1)
        context = f'Created at {created_at.strftime("%b %d %Y %H:%M:%S")}'
        if latest_update_created_at > max_time:
            context += f', Updated at {latest_update_created_at.strftime("%b %d %Y %H:%M:%S")}'

        message = [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Github Incident"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Github reported a `{impact}` incident and current status is `{status}`"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"```{latest_update_body}```"
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain_text",
                                "text": context
                            }
                        ]
                    }
                ]
            }
        ]

        return message

    def _send_to_listeners(self, message):
        channels = SlackBotChannel.objects.select_related('bot').filter(bot__is_active=True)

        for channel in channels:
            client = WebClient(token=channel.bot.bot_token)
            client.chat_postMessage(channel=channel.channel_id, attachments=message)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        if not data:
            return HttpResponse()

        message = None

        if 'incident' in data:
            message = self._process_incident(data)

        if message:
            self._send_to_listeners(message)

        return HttpResponse()


@csrf_exempt
def slack_events_handler(request: HttpRequest):
    return handler.handle(request)


@method_decorator(csrf_exempt, name='dispatch')
class SlackOAuthView(TemplateView):
    template_name = 'install.html'

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

        #---

        current_url = resolve(self.request.path_info).url_name
        code = self.request.GET.get('code')

        if current_url == 'oauth_redirect' and code:
            params = {
                'code': code,
                'client_id': settings.SLACK_CLIENT_ID,
                'client_secret': settings.SLACK_CLIENT_SECRET,
                'redirect_uri': redirect_uri
            }
            r = requests.get('https://slack.com/api/oauth.v2.access', params=params)
            r.raise_for_status()

            if (settings.DEBUG):
                print(r.url)
                print(r.text)

            data = r.json()

            if (not data.get('ok') or data.get('ok') == 'false' or not data.get('access_token')):
                raise PermissionDenied('Could not obtain access! (Reason: {0})'.format(data.get('error')))

            if (settings.DEBUG):
                print(data.get('access_token'))

            # save token response


            # show success
            context.update({
                'slack_workspace': data.get('team').get('name')
            })
            self.template_name='oauth_success.html'

        return context
