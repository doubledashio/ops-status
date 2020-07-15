import json
import logging

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class GithubWebhookView(View):
    def _process_incident(self, data):
        incident = data['incident']
        created_at = incident['created_at']
        impact = incident['impact']
        status = incident['status']
        latest_update = incident['incident_updates'][0]
        latest_update_body = latest_update['body']
        latest_update_created_at = latest_update['created_at']
        latest_update_status = latest_update['status']

        message = f'''  # noqa
Github reported a `{impact}` *incident* at {created_at}, current status is `{status}`.

Latest update provided at {latest_update_created_at} with status `{latest_update_status}`:
```
{latest_update_body}
```
        '''.strip()

        return message

    def _process_update(self, data):
        component = data['component']
        component_name = component['name']
        component_update = data['component_update']
        component_update_created_at = component_update['created_at']
        component_update_old_status = component_update['old_status']
        component_update_new_status = component_update['new_status']

        message = f'''
Component `{component_name}` status updated from `{component_update_old_status}` to `{component_update_new_status}` on `{component_update_created_at}`.
        '''

        return message

    def _send_to_listeners(self, message):
        print(message)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        if not data:
            return HttpResponse()

        message = None

        if 'incident' in data:
            message = self._process_incident(data)

        if 'component_update' in data:
            message = self._process_update(data)

        if message:
            self._send_to_listeners(message)

        return HttpResponse()
