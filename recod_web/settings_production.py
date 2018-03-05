from .settings import *

STATIC_ROOT = '/var/www/recod_web/staticfiles/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'recod_web.storage_backends.MediaStorage'

DEBUG = False
ENV = 'production'
