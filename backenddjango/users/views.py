from rest_framework import viewsets, status, filters, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView, GenericAPIView
from .models import User, Notification, NotificationPreference, EmailLog
from .serializers import (
    UserSerializer, UserCreateSerializer, NotificationSerializer, 
    NotificationListSerializer, NotificationPreferenceSerializer,
    UserLoginSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    LogoutSerializer, EmailLogSerializer, EmailPreviewSerializer, DownloadEmailLogsSerializer
)
from .permissions import IsAdmin, IsSelfOrAdmin
from .services import get_or_create_notification_preferences
from django.contrib.auth import authenticate
import logging
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiParameter

# Set up logger
logger = logging.getLogger(__name__)


@extend_schema(
    request=LogoutSerializer,
    responses={200: {"type": "object", "properties": {"detail": {"type": "string"}}}}
)
class LogoutView(GenericAPIView):
    """
    API endpoint for user logout
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer
    
    def post(self, request):
        try:
            # Get the refresh token from request data
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            logger.info(f"User {request.user.email} logged out successfully")
            return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return Response({"error": "Invalid token or token already blacklisted"}, 
                           status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=UserLoginSerializer,
    responses={200: {"type": "object", "properties": {"refresh": {"type": "string"}, "access": {"type": "string"}}}}
)
class LoginView(APIView):
    """
    API endpoint for user login
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        logger.info(f"Login attempt for email: {email}")
        
        # Try to authenticate with email
        user = authenticate(username=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            
            # Check if there's a next parameter for redirection
            next_url = request.query_params.get('next')
            if next_url:
                from django.shortcuts import redirect
                response = redirect(next_url)
                # Set the token as a cookie
                response.set_cookie(
                    'access_token', 
                    str(refresh.access_token), 
                    httponly=True, 
                    secure=False,  # Set to True in production with HTTPS
                    samesite='Lax'
                )
                return response
            
            # If no redirection, return the token as usual
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'email': user.email,
                'role': user.role,
                'name': f"{user.first_name} {user.last_name}".strip()
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    """
    API endpoint for user registration
    """
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    
    def post(self, request):
        try:
            # Log the incoming request data
            logger.info(f"Registration attempt with data: {request.data}")
            
            # Create user with email only, no username needed
            data = request.data.copy()
                
            serializer = UserCreateSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'email': user.email,
                    'role': user.role,
                    'name': f"{user.first_name} {user.last_name}".strip()
                }, status=status.HTTP_201_CREATED)
            
            # Log validation errors
            logger.error(f"Registration validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log any exceptions
            logger.exception(f"Exception during registration: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(RetrieveAPIView):
    """
    API endpoint for retrieving user profile
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class UserProfileUpdateView(UpdateAPIView):
    """
    API endpoint for updating user profile
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class NotificationListView(ListAPIView):
    """
    API endpoint for listing user notifications
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read', 'notification_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Notification.objects.none()
        return Notification.objects.filter(user=self.request.user)


class NotificationMarkReadView(APIView):
    """
    API endpoint for marking notifications as read
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def post(self, request):
        notification_id = request.data.get('notification_id')
        
        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id, user=request.user)
                notification.is_read = True
                notification.save()
                return Response({'status': 'notification marked as read'})
            except Notification.DoesNotExist:
                return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Mark all as read
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
            return Response({'status': 'all notifications marked as read'})


class NotificationCountView(APIView):
    """
    API endpoint for getting unread notification count
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationListSerializer
    
    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})


class NotificationPreferenceView(APIView):
    """
    API endpoint for managing notification preferences
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationPreferenceSerializer
    
    def get(self, request):
        """
        Get notification preferences for the current user
        """
        preferences = get_or_create_notification_preferences(request.user)
        serializer = NotificationPreferenceSerializer(preferences)
        return Response(serializer.data)
    
    def put(self, request):
        """
        Update notification preferences for the current user
        """
        preferences = get_or_create_notification_preferences(request.user)
        serializer = NotificationPreferenceSerializer(preferences, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users
    """
    queryset = User.objects.all().order_by('-date_joined')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            # Only admin users can list all users
            permission_classes = [IsAuthenticated, IsAdmin]
        elif self.action == 'retrieve':
            # Admin users can retrieve any user, other users can only retrieve themselves
            permission_classes = [IsAuthenticated, IsSelfOrAdmin]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only admin users can create, update, or delete users
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            # Default to authenticated users for other actions
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user information
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for managing notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read', 'notification_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Notification.objects.none()
        return Notification.objects.filter(user=self.request.user)
    
    @extend_schema(parameters=[OpenApiParameter("id", int, OpenApiParameter.PATH)])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NotificationListSerializer
        return NotificationSerializer
    
    @extend_schema(parameters=[OpenApiParameter("id", int, OpenApiParameter.PATH)])
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Mark a notification as read
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        
        # Send WebSocket update for unread count
        try:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            
            channel_layer = get_channel_layer()
            unread_count = self.get_queryset().filter(is_read=False).count()
            
            async_to_sync(channel_layer.group_send)(
                f"user_{request.user.id}_notifications",
                {
                    'type': 'notification_count',
                    'count': unread_count
                }
            )
        except Exception as e:
            # Log the error but don't fail the operation
            print(f"Error sending WebSocket notification: {str(e)}")
            
        return Response({'status': 'notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Mark all notifications as read
        """
        self.get_queryset().update(is_read=True)
        
        # Send WebSocket update for unread count
        try:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            
            channel_layer = get_channel_layer()
            
            async_to_sync(channel_layer.group_send)(
                f"user_{request.user.id}_notifications",
                {
                    'type': 'notification_count',
                    'count': 0
                }
            )
        except Exception as e:
            # Log the error but don't fail the operation
            print(f"Error sending WebSocket notification: {str(e)}")
            
        return Response({'status': 'all notifications marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Get count of unread notifications
        """
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})


@extend_schema(
    request=PasswordResetRequestSerializer,
    responses={200: {"type": "object", "properties": {"detail": {"type": "string"}}}}
)
class PasswordResetRequestView(APIView):
    """
    API endpoint for requesting a password reset
    """
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                
                # Generate token
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Build reset URL
                scheme = request.scheme
                host = request.get_host()
                reset_url = f"{scheme}://{host}/reset-password-confirm/?uid={uid}&token={token}"
                
                # Send email
                subject = "Password Reset Request"
                message = f"Please click the link below to reset your password:\n\n{reset_url}"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [email]
                
                send_mail(subject, message, from_email, recipient_list)
                
                logger.info(f"Password reset email sent to {email}")
                return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # Return success even if user doesn't exist for security reasons
                logger.info(f"Password reset requested for non-existent email: {email}")
                return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error sending password reset email: {str(e)}")
                return Response({"error": "Failed to send password reset email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=PasswordResetConfirmSerializer,
    responses={200: {"type": "object", "properties": {"detail": {"type": "string"}}}}
)
class PasswordResetConfirmView(APIView):
    """
    API endpoint for confirming a password reset
    """
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                # Decode the user ID
                user_id = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=user_id)
                
                # Verify the token
                token_generator = PasswordResetTokenGenerator()
                if token_generator.check_token(user, token):
                    # Set the new password
                    user.set_password(new_password)
                    user.save()
                    
                    logger.info(f"Password reset successful for user {user.email}")
                    return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
                else:
                    logger.warning(f"Invalid password reset token for user {user.email}")
                    return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                logger.warning(f"Invalid password reset UID: {uid}")
                return Response({"error": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Error during password reset: {str(e)}")
                return Response({"error": "Failed to reset password."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EmailPreviewView(APIView):
    """
    View for previewing email templates in development mode.
    Only available when DEBUG=True.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = EmailPreviewSerializer
    
    def get(self, request):
        if not settings.DEBUG:
            return Response(
                {"detail": "Email preview is only available in development mode"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        template_name = request.query_params.get('template')
        if not template_name:
            return Response(
                {"detail": "Template name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Basic context for testing
        context = {
            'user': request.user,
            'notifications': Notification.objects.filter(user=request.user)[:5],
            'notification_count': 5,
            'date': timezone.now().strftime('%Y-%m-%d'),
            'start_date': (timezone.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'end_date': timezone.now().strftime('%Y-%m-%d')
        }
        
        try:
            from users.services import preview_email
            html_content = preview_email(template_name, context)
            return HttpResponse(html_content)
        except Exception as e:
            return Response(
                {"detail": f"Error rendering template: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class DownloadEmailLogsView(APIView):
    """
    View for downloading email logs as a DOCX file.
    Only available to admin users.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = DownloadEmailLogsSerializer
    
    def get(self, request):
        from crm_backend.tasks import export_email_logs_to_docx
        
        # Get log IDs from query params
        log_ids = request.query_params.getlist('ids')
        if not log_ids:
            return Response(
                {"detail": "No email logs selected for export"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert string IDs to integers
        try:
            log_ids = [int(log_id) for log_id in log_ids]
        except ValueError:
            return Response(
                {"detail": "Invalid log ID format"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate DOCX file
        output = export_email_logs_to_docx(log_ids)
        
        # Create response with the DOCX file
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename="email_logs_export.docx"'
        return response
