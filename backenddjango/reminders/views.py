from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Reminder
from .serializers import ReminderSerializer
from users.permissions import IsAdminOrBrokerOrBD


class ReminderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing reminders
    """
    queryset = Reminder.objects.all().order_by('send_datetime')
    serializer_class = ReminderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['subject', 'email_body', 'recipient_email']
    filterset_fields = ['recipient_type', 'is_sent', 'related_application', 'related_borrower']
    
    def get_permissions(self):
        """
        Only authenticated users with admin, broker, or BD roles can manage reminders
        """
        permission_classes = [IsAuthenticated, IsAdminOrBrokerOrBD]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter reminders based on user role
        """
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter reminders based on user role
        if user.role == 'admin':
            return queryset
        elif user.role in ['broker', 'bd']:
            # Users can see reminders they created
            return queryset.filter(created_by=user)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        """
        Set the created_by field to the current user
        """
        serializer.save(created_by=self.request.user)