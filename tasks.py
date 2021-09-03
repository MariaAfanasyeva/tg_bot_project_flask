from __future__ import absolute_import
from app import app, make_celery, s3
import os
import boto3
from moviepy.editor import VideoFileClip


app.config.update(
    CELERY_BROCKER_URL=os.environ.get("CELERY_BROKER_URL"),
    CELERY_RESULT_BACKEND=os.environ.get("CELERY_RESULT_BACKEND"),
)

celery = make_celery(app)


@celery.task
def resize_video(key):
    try:
        s3.download_file("flask-video-tg", key, key)
        try:
            glacier = boto3.client(
                "glacier",
                aws_access_key_id=os.environ.get("ACCESS_KEY"),
                aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
            )
            glacier.upload_archive(
                vaultName="tg_flask_source_videos", body=open(key, "rb")
            )

        except Exception as e:
            print(e)
        my_video = VideoFileClip(key)
        resized_video = my_video.resize((640, 480))
        resized_video.write_videofile(key)
        try:
            s3.upload_file(Filename=key, Bucket="flask-video-tg", Key=key)
            os.remove(key)
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
