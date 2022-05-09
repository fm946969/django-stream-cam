from django.http import HttpRequest
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .models import VideoCam
from asgiref.sync import sync_to_async
from channels.http import AsgiRequest

# Create your views here.
def index(request:HttpRequest):
    if request.user.is_authenticated:
        return render(request, 'index.html',{'hi':'auth'})
    else:
        return render(request, 'index.html',{'hi':'not auth'})
    
def gen(response:StreamingHttpResponse):
    print(f'{type(response) = } ')
    camera = VideoCam()
    
    while not response.closed:
        frame = camera.read()
        yield (b'--frame\r\n' 
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    print('this is video_feed')
    response = StreamingHttpResponse(content_type='multipart/x-mixed-replace; boundary=frame')
    response.streaming_content = gen(response)
    return response