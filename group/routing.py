from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .views import GroupConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chat/<str:room_name>/', GroupConsumer.as_asgi()),
    ]),
})