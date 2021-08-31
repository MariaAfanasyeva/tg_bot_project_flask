import boto3
import os
from moviepy.editor import VideoFileClip

s3 = boto3.client("s3", aws_access_key_id=os.environ.get("ACCESS_KEY"),
                  aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"))

try:
    s3.download_file("flask-video-tg", "Piano_Playing_Close.mp4", "Piano_Playing_Close.mp4")
    my_video = VideoFileClip("Piano_Playing_Close.mp4")
    resized_video = my_video.resize((640, 480))
    resized_video.write_videofile("resized_piano.mp4")
except Exception as e:
    print(e)
