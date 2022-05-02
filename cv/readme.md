Create venv
Install Django and create a project
Create an app call ‘cam’
In app ‘cam’, Create a model ‘VideoCam’ for handling video capture
In app ‘cam’ -> ‘views.py’, create two view handles (index + video feed)
In app ‘cam’, create ‘url.py’
Add path -> index
Add path -> video feed
In main settings.py, add installed app ‘cam.apps.CamConfig’
In main urls.py, include ‘cam.urls’
