from asyncore import loop, read
from datetime import datetime, date, timedelta
from email.message import Message
import cv2
from cv2 import VideoWriter_fourcc
from django.db import models
import asyncio
import threading
import time
import numpy
import base64

# Create your models here.
class Msg:
    Messages = []
    def __init__(self, msg = 'Hi', x = 0 , y = 0, life = 2, id:int = -1) -> None:
        self.expire = datetime.now() + timedelta(seconds=life)
        self.x = x
        self.y = y
        self.msg = msg
        if id == -1:
            Msg.Messages.append(self)
        elif len(Msg.Messages) > id:
            Msg.Messages[id] = self
        else:
            Msg.Messages.append(self)
    @classmethod
    def update(cls, img):
        for msg in cls.Messages:
            if datetime.now() > msg.expire:
                msg.Messages.remove(msg)
            else:
                img = cv2.putText(img, msg.msg, (msg.x, msg.y), cv2.FONT_HERSHEY_PLAIN, 1, (64,64,255), 1)
        return img

class VideoCam():#models.Model):
    expire = datetime(2000,1,1)
    def __init__(self):
        now:datetime = datetime.now()
        print('Starting cam')
            
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        print('Cam started')

        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        size = (width, height)
        print(f'{size = }, {fps = }')
        if fps == 0:
            fps = 30

        self.frame = numpy.zeros((width,height,3))
        
        self.video = cv2.VideoWriter(f'{now.strftime("%Y-%m-%d-%H-%M-%S")}.avi', VideoWriter_fourcc(*'FMP4'),fps,size)
        print('Start recording')
        self.consumers = []
        self.run = False
        self.record = True
        self.capture = True
        self.start_thread()
    
    def start_thread(self):
        if not self.run:
            self.run = True
            self.task = threading.Thread(target=self.loop)
            self.task.start()
    def loop(self):
        while self.run:
            if self.capture:
                ret, frame = self.cap.read()
                if ret:
                    self.frame = frame
                    if self.record:
                        self.video.write(frame)
                else:
                    frame = self.frame
                    if self.record:
                        self.video.write(frame)
    def toggle_record(self, record):
        self.record = record
    def toggle_capture(self, capture):
        self.capture = capture
    def add_consumer(self, consumer):
        self.start_thread()
        self.consumers.append(consumer)

    def remove_consumer(self, consumer):
        self.consumers.remove(consumer)
        if len(self.consumers) == 0:
            self.run = False
            VideoCam.expire = datetime.now() + timedelta(seconds=5)

    def read(self):
        ret, jpeg = cv2.imencode('.jpg', Msg.update(self.frame))
        return jpeg.tobytes()
    def __del__(self):
        print('release')
        self.run = False
        # self.task.join()