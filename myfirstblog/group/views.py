from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Group, Message
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group/group_list.html', {'groups': groups})


@login_required
def group_chat(request, pk):
    group = get_object_or_404(Group, pk=pk)
    messages = Message.objects.filter(group=group).order_by('date_create')
    
    if request.user not in group.user_list.all():
        group.user_list.add(request.user)
    
    context = {
        'group': group,
        'messages': messages,
        'room_name': group.pk
    }
    return render(request, 'group/chat.html', context)


@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            group = Group.objects.create(name=name)
            group.user_list.add(request.user)
            return redirect('group_chat', pk=group.pk)
    return render(request, 'group/create_group.html')

@login_required
@csrf_exempt
def upload_image(request):
    """API для загрузки изображений в чат"""
    if request.method == 'POST':
        try:
            group_id = request.POST.get('group_id')
            image_file = request.FILES.get('image')
            
            if not group_id or not image_file:
                return JsonResponse({'error': 'Отсутствуют обязательные параметры'}, status=400)
            
            # Проверяем, что группа существует и пользователь в ней состоит
            group = get_object_or_404(Group, pk=group_id)
            if request.user not in group.user_list.all():
                return JsonResponse({'error': 'Нет доступа к этой группе'}, status=403)
            
            # Проверяем тип файла
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if image_file.content_type not in allowed_types:
                return JsonResponse({'error': 'Неподдерживаемый тип файла'}, status=400)
            
            # Проверяем размер файла (максимум 5MB)
            if image_file.size > 5 * 1024 * 1024:
                return JsonResponse({'error': 'Файл слишком большой (максимум 5MB)'}, status=400)
            
            # Создаем сообщение с изображением
            message = Message.objects.create(
                text='',  
                img=image_file,
                author=request.user,
                group=group
            )
            
            return JsonResponse({
                'success': True,
                'message_id': message.id,
                'image_url': message.img.url,
                'author': request.user.username,
                'group_id': group_id
            })
            
        except Exception as e:
            return JsonResponse({'error': f'Ошибка загрузки: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

class GroupConsumer(AsyncWebsocketConsumer):    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Проверяем, что пользователь аутентифицирован
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name)  
    
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'text')
            
            if message_type == 'text':
                message = text_data_json.get('message', '')
                
                if not message.strip():
                    return
                
                # Получаем имя пользователя из scope
                username = self.scope["user"].username
                
                # Сохраняем сообщение в базу данных
                await self.save_message(message, username, self.room_name)
                
                # Отправляем сообщение в группу
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'author': username,
                        'message_type': 'text'
                    }
                )
            
            elif message_type == 'image':
                # Обработка уведомлений о новых изображениях
                image_url = text_data_json.get('image_url', '')
                message_id = text_data_json.get('message_id', '')
                username = self.scope["user"].username
                
                if image_url and message_id:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'image_url': image_url,
                            'author': username,
                            'message_type': 'image',
                            'message_id': message_id
                        }
                    )
        
        except json.JSONDecodeError:
            pass
        except Exception as e:
            traceback.print_exc()
    
    async def chat_message(self, event):
        message_type = event.get('message_type', 'text')
        author = event['author']
        
        if message_type == 'text':
            message = event['message']
            await self.send(text_data=json.dumps({
                'message': message,
                'author': author,
                'message_type': 'text'
            }))
        elif message_type == 'image':
            # Отправка уведомления о новом изображении
            image_url = event['image_url']
            message_id = event.get('message_id', '')
            await self.send(text_data=json.dumps({
                'image_url': image_url,
                'author': author,
                'message_type': 'image',
                'message_id': message_id
            }))
    
    @database_sync_to_async
    def save_message(self, message_text, username, room_name):
        try:
            user = User.objects.get(username=username)
            group = Group.objects.get(pk=room_name)
            Message.objects.create(
                text=message_text,
                author=user,
                group=group
            )
            return True
        except (User.DoesNotExist, Group.DoesNotExist) as e:
            return False
        except Exception as e:
            return False