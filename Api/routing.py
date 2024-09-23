from django.urls import re_path, path

from Api.consumers import ApiConsumer

websocket_urlpatterns = [
    path("api/", ApiConsumer.as_asgi()),
]