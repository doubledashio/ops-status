from .base import *  # noqa

# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
SECRET_KEY = env("SECRET_KEY")  # noqa
X_FRAME_OPTIONS = "DENY"

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = ["*"]

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES[0]["APP_DIRS"] = False  # noqa
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    ),
]

# SESSION
# ------------------------------------------------------------------------------
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_COOKIE_AGE = 10800  # 3 hours

# MESSAGE
# ------------------------------------------------------------------------------
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# django-q
# ------------------------------------------------------------------------------
Q_CLUSTER = {
    "cpu_affinity": 1,
    "django_redis": "default",
    "label": "Django Q",
    "name": "ops_status",
    "save_limit": -1,
    "timeout": 30,
    "workers": 4,
}

# django-storages
# ------------------------------------------------------------------------------
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")  # noqa
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")  # noqa
AWS_S3_REGION_NAME = "us-east-1"
AWS_STORAGE_BUCKET_NAME = env("AWS_BUCKET_NAME")  # noqa
AWS_LOCATION = env("AWS_LOCATION")  # noqa
AWS_IS_GZIPPED = True
AWS_DEFAULT_ACL = "public-read"

_BASE_ASSETS_ENDPOINT = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{AWS_LOCATION}"

DEFAULT_FILE_STORAGE = "config.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"{_BASE_ASSETS_ENDPOINT}/media/"

STATICFILES_STORAGE = "config.storages.StaticRootS3Boto3Storage"
STATIC_URL = f"{_BASE_ASSETS_ENDPOINT}/static/"
