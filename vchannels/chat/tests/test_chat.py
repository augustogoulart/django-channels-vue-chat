import random
import string
import pytest
from django.conf import settings
from channels.routing import ProtocolTypeRouter
from channels.testing import WebsocketCommunicator

from vchannels.routing import application
from ..consumers import ChatConsumer


def generate_random_room_name():
    return ''.join(
        random.choice(
            string.ascii_letters) for i in range(
            random.choice(range(64))
        )
    )


def test_websocket_layer_exists():
    """
    Root level ASGI application exists

    Channels need a root ASGI application to run.
    Routers are themselves valid ASGI applications
    """
    assert settings.ASGI_APPLICATION


def test_root_asgi_application_type():
    """
    The Channels documentation recommends the root application to be a ProtocolTypeRouter
    """
    assert isinstance(application, ProtocolTypeRouter)


def test_room_chat_get(client):
    response = client.get(f'/chat/{generate_random_room_name()}')
    assert response.status_code == 200


def test_template_used(client):
    response = client.get(f'/chat/{generate_random_room_name()}')
    templates = response.templates
    assert 'chat/room.html' in [template.name for template in templates]


def test_room_page_displays_room_name(client):
    room_name = generate_random_room_name()
    response = client.get(f'/chat/{room_name}')
    assert room_name.encode() in response.content


@pytest.mark.asyncio
async def test_consumer_accepts_connection():
    communicator = WebsocketCommunicator(ChatConsumer, "/ws/chat/room")
    connected, subprotocol = await communicator.connect()
    assert connected
