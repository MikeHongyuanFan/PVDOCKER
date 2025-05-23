from rest_framework import serializers
from .models import User, Notification, NotificationPreference, EmailLog
from django.contrib.auth.password_validation import validate_password


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request
    """
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation
    """
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone']
        read_only_fields = ['id']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating users
    """
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)
    branch_id = serializers.IntegerField(required=False, write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role', 'phone', 'username', 'branch_id']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        branch_id = validated_data.pop('branch_id', None)
        
        # Set username to email if not provided
        if 'username' not in validated_data or not validated_data['username']:
            validated_data['username'] = validated_data['email']
            
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create default notification preferences for the user
        NotificationPreference.objects.create(user=user)
        
        # If user role is BD, create BDM profile
        if user.role == 'bd':
            from brokers.models import BDM, Branch
            
            try:
                branch = None
                if branch_id:
                    branch = Branch.objects.get(id=branch_id)
                
                # Create BDM profile
                BDM.objects.create(
                    user=user,
                    name=f"{user.first_name} {user.last_name}".strip() or user.email,
                    email=user.email,
                    phone=user.phone,
                    branch=branch,
                    created_by=self.context.get('request').user if self.context.get('request') else None
                )
            except Branch.DoesNotExist:
                # If branch doesn't exist, still create BDM but without branch
                BDM.objects.create(
                    user=user,
                    name=f"{user.first_name} {user.last_name}".strip() or user.email,
                    email=user.email,
                    phone=user.phone,
                    created_by=self.context.get('request').user if self.context.get('request') else None
                )
        
        return user


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model
    """
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['created_at']


class NotificationListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing notifications
    """
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'notification_type', 'notification_type_display', 'is_read', 'created_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for NotificationPreference model
    """
    class Meta:
        model = NotificationPreference
        exclude = ['user', 'created_at', 'updated_at']
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout endpoint
    """
    refresh = serializers.CharField(required=True, help_text="Refresh token to blacklist")
class EmailLogSerializer(serializers.ModelSerializer):
    """
    Serializer for EmailLog model
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = EmailLog
        fields = ['id', 'user', 'user_email', 'subject', 'sent_at', 'status', 'status_display', 
                  'notification', 'email_type']
        read_only_fields = ['id', 'sent_at', 'user_email', 'status_display']

class EmailPreviewSerializer(serializers.Serializer):
    """
    Serializer for email preview endpoint
    """
    template = serializers.CharField(required=True, help_text="Template name to preview")


class DownloadEmailLogsSerializer(serializers.Serializer):
    """
    Serializer for downloading email logs endpoint
    """
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="List of email log IDs to export"
    )
