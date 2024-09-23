import json
import channels_graphql_ws
from channels.generic.websocket import WebsocketConsumer
from Api.schema import schema


class ApiConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """GraphQL WebSocket consumer."""

    schema = schema