from contextlib import nullcontext
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .models import VideoCam

# Create your views here.
cam = None
def index(request):
    print(f'this is index {type(request) = }')
    return render(request, 'index.html',{'hi':'wow i am here'})
    
def gen(camera:VideoCam):
    while True:
        frame = camera.read()
        yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    print('this is video_feed')
    request
    return StreamingHttpResponse(gen(VideoCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')