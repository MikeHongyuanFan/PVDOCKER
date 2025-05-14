from rest_framework import serializers
from .models import Reminder
from users.models import User


class ReminderSerializer(serializers.ModelSerializer):
    """
    Serializer for reminders
    """
    created_by_name = serializers.StringRelatedField(source='created_by')
    send_as_user_email = serializers.SerializerMethodField()
    reply_to_user_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Reminder
        fields = [
            'id', 'recipient_type', 'recipient_email', 'send_datetime', 
            'email_body', 'subject', 'created_by', 'created_by_name',
            'send_as_user', 'send_as_user_email', 'reply_to_user', 
            'reply_to_user_email', 'is_sent', 'sent_at', 'error_message',
            'related_application', 'related_borrower', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'is_sent', 'sent_at', 'error_message', 'created_at', 'updated_at']
    
    def get_send_as_user_email(self, obj) -> str:
        if obj.send_as_user:
            return obj.send_as_user.email
        return None
    
    def get_reply_to_user_email(self, obj) -> str:
        if obj.reply_to_user:
            return obj.reply_to_user.email
        return None
    
    def validate_send_as_user(self, value):
        """
        Validate that the user has permission to send as this user
        """
        if value:
            request = self.context.get('request')
            if request and request.user:
                # Only admin and BD roles can send as other users
                if request.user.role not in ['admin', 'bd']:
                    raise serializers.ValidationError("You don't have permission to send emails as other users")
                
                # Users can always send as themselves
                if request.user.id == value.id:
                    return value
                
                # Admin can send as anyone
                if request.user.role == 'admin':
                    return value
                
                # BD can only send as themselves or their assistants
                if request.user.role == 'bd':
                    # This is a simplified check - in a real system, you might have a more complex relationship model
                    raise serializers.ValidationError("BD users can only send as themselves")
        
        return value