import pytest
from django.conf import settings
from channels.routing import ProtocolTypeRouter

from vchannels.routing import application


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
