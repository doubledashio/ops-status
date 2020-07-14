from django.conf import settings
from django.core.files.storage import get_storage_class, FileSystemStorage

from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = f'{getattr(settings, "AWS_LOCATION", "")}/static'
    object_parameters = {
        'CacheControl': f'max-age=604800, s-maxage=604800, must-revalidate'  # Cache for a week
    }
    querystring_auth = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_storage = get_storage_class('compressor.storage.CompressorFileStorage')()

    def save(self, name, content):
        self.local_storage._save(name, content)
        name = super().save(name, self.local_storage._open(name))
        return name


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = f'{getattr(settings, "AWS_LOCATION", "")}/media'
    object_parameters = {
        'CacheControl': f'max-age=1800, s-maxage=1800, must-revalidate'  # Cache for 30m
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StaticRootFileSystemStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'location': 'static'
        })
        super().__init__(*args, **kwargs)


class MediaRootFileSystemStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'location': 'media'
        })
        super().__init__(*args, **kwargs)
