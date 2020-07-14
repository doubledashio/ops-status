from .staging import *  # noqa

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# SENTRY
# ------------------------------------------------------------------------------
sentry_sdk.init(
    dsn='https://27c5796204ee42c8a82b4d2619cddf69@sentry.io/1827203',
    integrations=[DjangoIntegration()]
)

# Logging Configuration
# ------------------------------------------------------------------------------
LOGGING['handlers']['console']['level'] = 'INFO'  # noqa
LOGGING['loggers']['project']['level'] = 'INFO'  # noqa
