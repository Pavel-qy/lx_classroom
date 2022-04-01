import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class CourseConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope['user'].is_anonymous:
            self.close()
        else:
            self.group_name = str(self.scope['user'].id)
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name,
            )
            self.accept()

    def disconnect(self, close_code):
        self.close()
    
    def notify(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
