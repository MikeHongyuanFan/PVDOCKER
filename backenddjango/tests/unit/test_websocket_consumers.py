"""
Unit tests for WebSocket consumers.
"""

import pytest
import json
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from users.consumers import NotificationConsumer
from users.models import Notification, NotificationPreference
from users.services import create_notification

User = get_user_model()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestNotificationConsumer:
    """Test the notification WebSocket consumer."""
    
    async def test_connect_authenticated(self, client_user):
        """Test connecting to the WebSocket as an authenticated user."""
        # Create a communicator with the authenticated user
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(),
            "/ws/notifications/",
            {"user": client_user}
        )
        
        # Connect to the WebSocket
        connected, _ = await communicator.connect()
        
        # Verify connection was successful
        assert connected
        
        # Verify initial unread count message
        response = await communicator.receive_json_from()
        assert response["type"] == "unread_count"
        assert response["count"] == 0
        
        # Disconnect
        await communicator.disconnect()
    
    async def test_connect_unauthenticated(self):
        """Test connecting to the WebSocket as an unauthenticated user."""
        # Create a communicator with an anonymous user
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(),
            "/ws/notifications/",
            {"user": None}
        )
        
        # Connect to the WebSocket (should fail)
        connected, _ = await communicator.connect()
        
        # Verify connection was rejected
        assert not connected
    
    async def test_receive_get_unread_count(self, client_user):
        """Test receiving a get_unread_count message."""
        # Create a notification for the user
        await database_sync_to_async(Notification.objects.create)(
            user=client_user,
            title="Test Notification",
            message="This is a test notification",
            notification_type="system"
        )
        
        # Create a communicator with the authenticated user
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(),
            "/ws/notifications/",
            {"user": client_user}
        )
        
        # Connect to the WebSocket
        connected, _ = await communicator.connect()
        assert connected
        
        # Receive initial unread count
        response = await communicator.receive_json_from()
        assert response["type"] == "unread_count"
        assert response["count"] == 1
        
        # Send get_unread_count message
        await communicator.send_json_to({
            "type": "get_unread_count"
        })
        
        # Receive updated unread count
        response = await communicator.receive_json_from()
        assert response["type"] == "unread_count"
        assert response["count"] == 1
        
        # Disconnect
        await communicator.disconnect()
    
    async def test_notification_message(self, client_user):
        """Test receiving a notification message."""
        # Create a communicator with the authenticated user
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(),
            "/ws/notifications/",
            {"user": client_user}
        )
        
        # Connect to the WebSocket
        connected, _ = await communicator.connect()
        assert connected
        
        # Receive initial unread count
        await communicator.receive_json_from()
        
        # Create a notification for the user
        notification = await database_sync_to_async(create_notification)(
            user=client_user,
            title="Real-time Notification",
            message="This notification should be delivered via WebSocket",
            notification_type="system"
        )
        
        # Receive the notification message
        response = await communicator.receive_json_from()
        assert response["type"] == "notification"
        assert response["notification"]["title"] == "Real-time Notification"
        assert response["notification"]["message"] == "This notification should be delivered via WebSocket"
        
        # Receive the updated unread count
        response = await communicator.receive_json_from()
        assert response["type"] == "unread_count"
        assert response["count"] == 1
        
        # Disconnect
        await communicator.disconnect()
    
    async def test_notification_count_update(self, client_user):
        """Test receiving a notification count update."""
        # Create a communicator with the authenticated user
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(),
            "/ws/notifications/",
            {"user": client_user}
        )
        
        # Connect to the WebSocket
        connected, _ = await communicator.connect()
        assert connected
        
        # Receive initial unread count
        await communicator.receive_json_from()
        
        # Create multiple notifications
        for i in range(3):
            await database_sync_to_async(Notification.objects.create)(
                user=client_user,
                title=f"Test Notification {i+1}",
                message=f"This is test notification {i+1}",
                notification_type="system"
            )
            
            # Receive notification message and count update
            await communicator.receive_json_from()  # notification message
            count_response = await communicator.receive_json_from()  # count update
            assert count_response["type"] == "unread_count"
            assert count_response["count"] == i + 1
        
        # Disconnect
        await communicator.disconnect()
    
    async def test_disconnect(self, client_user):
        """Test disconnecting from the WebSocket."""
        # Create a communicator with the authenticated user
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(),
            "/ws/notifications/",
            {"user": client_user}
        )
        
        # Connect to the WebSocket
        connected, _ = await communicator.connect()
        assert connected
        
        # Receive initial unread count
        await communicator.receive_json_from()
        
        # Disconnect
        await communicator.disconnect()
        
        # Verify the connection is closed
        with pytest.raises(Exception):
            await communicator.receive_from()
