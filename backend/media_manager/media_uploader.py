import boto3
from django.conf import settings
import base64


def upload_image(b64_image, type, folder, filename):
    image_data = base64.b64decode(b64_image)

    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
                        region_name=settings.AWS_S3_REGION_NAME)
    filename = filename.replace(' ', '')
    try:
        s3.Bucket(settings.AWS_S3_STORAGE_BUCKET_NAME).put_object(Key=f'{folder}/{filename}.{type}',
                                                                  Body=image_data)
    except Exception as e:
        return e

    return f'https://{settings.AWS_S3_STORAGE_BUCKET_NAME}.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{folder}/{filename}.{type}'


class media_uploader:
    pass
