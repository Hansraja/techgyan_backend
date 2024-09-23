from django.urls import re_path, path

from Api.consumers import ApiConsumer

websocket_urlpatterns = [
    path("ws/graphql", ApiConsumer.as_asgi()),
]