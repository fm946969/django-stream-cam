from datetime import datetime, date
import cv2
from cv2 import VideoWriter_fourcc
from django.db import models

# Create your models here.
class VideoCam(models.Model):
    def __init__(self):

        now:datetime = datetime.now()
        self.cap = cv2.VideoCapture(1)

        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (width, height)
        
        self.video = cv2.VideoWriter(f'{now.strftime("%Y-%m-%d-%H-%M-%S")}.mp4', VideoWriter_fourcc('M','P','4','V'),self.cap.get(cv2.CAP_PROP_FPS),size)
    
    def read(self):
        ret, frame = self.cap.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        self.video.write(frame)
        return jpeg.tobytes()
    
    def __del__(self):
        self.video.release()
        self.cap.release()