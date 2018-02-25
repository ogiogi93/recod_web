from storages.backends.s3boto3 import S3Boto3Storage

from recod_web.settings import AWS_STORAGE_BUCKET_NAME


class MediaStorage(S3Boto3Storage):
    location = AWS_STORAGE_BUCKET_NAME + '/media'
    file_overwrite = True
