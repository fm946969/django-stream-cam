import atexit
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from cam.models import VideoCam, Msg
import base64

class FirstConsumer(AsyncJsonWebsocketConsumer):
    group_name = 'any'
    channel_name = 'any'
    cam = VideoCam()
    # import sys
    # f = sys._getframe()
    # while f.f_back != None:
    #     print(f'{f.f_code.co_filename} {f.f_lineno} {f.f_back}')
    #     f = f.f_back

    async def connect(self):
        await self.accept()
        FirstConsumer.cam.add_consumer(self)
        print(f'accepted')

    async def disconnect(self, close_code):
        print(f'disconnected {close_code = }')
        FirstConsumer.cam.remove_consumer(self)

    async def receive_json(self, obj):
        #print(f'{obj["type"] = }')
        if obj['type'] == 'vid?':
            await self.reply_cam_image()
            return
        elif obj['type'] == 'cmd_camera':
            if obj['cmd'] == 'cam_on':
                self.cam.toggle_capture(True)
            elif obj['cmd'] == 'cam_off':
                self.cam.toggle_capture(False)
            elif obj['cmd'] == 'rec_on':
                self.cam.toggle_record(True)
            elif obj['cmd'] == 'rec_off':
                self.cam.toggle_record(False)
            return
        elif obj['type'] == 'key_down':
            print(f'key_down {obj["type"] = }')
            self.onKeyDown(obj['key_code'])
            return
        elif obj['type'] == 'key_up':
            print(f'key_up {obj["type"] = }')
            self.onKeyUp(obj['key_code'])
            return
        else:
            print(f'???? {obj["type"] = }')

        print(f'{obj = }')
        
        message = obj['message']
        print(f'{message = }')

        await self.send_json(
            {
                'type': 'msg',
                'message': message
            }
        )
        print('replied')
    
    async def reply_cam_image(self):
        reply = {
            'type': 'cam',
            'cam': base64.b64encode(self.cam.read()).decode('utf-8')
        }
        #print(json.dumps(reply)[:200])
        await self.send_json(reply)
    def onKeyDown(self, key_code):
        print(f'{key_code = }')
        Msg(chr(key_code), 100,100, id=0)
    def onKeyUp(self, key_code):
        print(f'{key_code = }')
        Msg(chr(key_code), 150,100, id=1)
