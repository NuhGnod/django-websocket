import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("self.scope.session : {}".format(self.scope['session'].keys()))
        print("self.user : {}".format(self))
        print("self.scope.user : {}".format(self.scope['user'].pk))
        print("AsyncWebSocketConsumer : {}".format(AsyncWebsocketConsumer))
        print("self.scope : {}".format(self.scope))
        print("self.channel_name : {}".format(self.channel_name))
    	# 파라미터 값으로 채팅 룸을 구별
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # 룸 그룹에 참가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        # 룸 그룹 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 웹소켓으로부터 메세지 받음

    async def receive(self, text_data):
        print("self.channel_name : {}".format(self.channel_name))
        print(self)
        a = ['1','2']
        a.append('3')
        print(a)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data)
        print("web socket")
        l = list(text_data_json.items())
        print(l)
        if cache.get('chat_data'):
            print("exist")
            caches = cache.get('chat_data')
            print(caches)
            print(type(a))
            print(type(caches))
            caches.append(l)
            print(caches)
            cache.set('chat_data', caches)

        else:
            cache.set('chat_data',l)
        datas = cache.get('chat_data')
        print(type(text_data_json))
        # 룸 그룹으로 메세지 보냄
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'id' : text_data_json['user_id']
            }
        )
        # await self.send(text_data=json.dumps({ #이러면 상대방에겐 안가고 나한테만 보내짐.
        #     'message': datas,
        #     'id' : text_data_json['user_id']
        #
        # }))
    # 룸 그룹으로부터 메세지 받음
    async def chat_message(self, event):
        message = event['message']
        print("room")
        # 웹소켓으로 메세지 보냄
        await self.send(text_data=json.dumps({
            'message': message,
            'id': event['id']

        }))