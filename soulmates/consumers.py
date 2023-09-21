import json
from channels.generic.websocket import AsyncWebsocketConsumer
from soulmates.models import public_room_chat_messages, public_chat_room, Member,private_chat,private_chat_messages
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connection accepted")
        self.room_name = self.scope['url_route']['kwargs']['roomname']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("WebSocket connection closed")

    async def get_or_create_room(self, room_id):
        try:
            return await database_sync_to_async(public_chat_room.objects.get)(id=room_id)
        except public_chat_room.DoesNotExist:
            return await database_sync_to_async(public_chat_room.objects.create)(id=room_id)

    async def get_or_create_private_room(self, id):
        return await database_sync_to_async(private_chat.objects.get)(id=id)

    async def get_member(self, user_id):
        return await database_sync_to_async(Member.objects.get)(id=user_id)

    async def create_message(self, user_id, current_room, message):
        return await database_sync_to_async(public_room_chat_messages.objects.create)(user=user_id, room=current_room, content=message)


    async def create_private_message(self, current_room, message,receiver_instance,member):
        return await database_sync_to_async(private_chat_messages.objects.create)(private_chat=current_room, content=message,message_sender=member,message_receiver=receiver_instance)


    async def get_messages(self, current_room):
        return await database_sync_to_async(public_room_chat_messages.objects.filter)(room=current_room)


    async def get_private_messages(self, current_room):
        return await database_sync_to_async(private_chat_messages.objects.filter)(private=current_room)


    async def receive(self, text_data):
        print("Received message")
        data = json.loads(text_data)
        message = data.get("message")
        room_id = data.get("roomId")
        userid = data.get("userid")
        room_name = data.get('roomname')
        is_room = data.get('is_room')
        is_private = data.get('is_private')
        receiver=data.get('receiver')
        print("receiver ",receiver)
        receiver=int(receiver)
        is_room = int(is_room)
        is_private = int(is_private)
        if is_room:
            try:
                member = await self.get_member(userid)
                current_room = await self.get_or_create_room(room_id)
                new_message = await self.create_message(member, current_room, message)
                print("Message saved")
            except Exception as e:
                print("Exception:", e)
            try:
                messages = await self.get_messages(current_room)
                messages = list(messages.order_by('id'))
            except:
                messages = []

            # Send the newly created message to the current WebSocket connection
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': new_message.content,
                }
            )
        if is_private:
            print("private message found ra")
            try:
                member = await self.get_member(userid)
                print("1")
                try:
                    receiver_instance = await self.get_member(receiver)
                except:
                    receiver_instance = member
                print("2")
                private_chat_room = await self.get_or_create_private_room(room_id)
                print("3")
                new_message = await self.create_private_message(private_chat_room, message,receiver_instance,member)
                print("4")
                print("Message saved")
            except Exception as e:
                print("Exception:", e)
            try:
                messages = await self.get_private_messages(private_chat_room)
                messages = list(messages.order_by('id'))
            except:
                messages = []

            # Send the newly created message to the current WebSocket connection
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': new_message.content,
                }
            )
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
        }))

