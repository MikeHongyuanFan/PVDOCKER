"""
Factory for Notification model.
"""

import factory
from factory.django import DjangoModelFactory
from users.models import Notification
from .user_factory import UserFactory
from .application_factory import ApplicationFactory


class NotificationFactory(DjangoModelFactory):
    """
    Base factory for Notification model.
    """
    
    class Meta:
        model = Notification
    
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=4)
    message = factory.Faker('paragraph')
    is_read = False
    notification_type = 'info'
    created_at = factory.Faker('date_time_this_month')
    
    @factory.post_generation
    def related_object(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            self.related_object_id = extracted.id
            self.related_object_type = extracted.__class__.__name__


class ApplicationStatusNotificationFactory(NotificationFactory):
    """
    Factory for application status notifications.
    """
    
    notification_type = 'application_status'
    title = 'Application Status Update'
    
    @factory.post_generation
    def application_status(self, create, extracted, **kwargs):
        if not create:
            return
            
        application = extracted if extracted else ApplicationFactory()
        self.message = f'The status of application #{application.reference_number} has been updated to {application.stage.capitalize()}.'
        self.related_object_id = application.id
        self.related_object_type = 'Application'


class DocumentRequestNotificationFactory(NotificationFactory):
    """
    Factory for document request notifications.
    """
    
    notification_type = 'document_request'
    title = 'Document Request'
    
    @factory.post_generation
    def document_request(self, create, extracted, **kwargs):
        if not create:
            return
            
        application = extracted if extracted else ApplicationFactory()
        self.message = f'Please upload the required documents for application #{application.reference_number}.'
        self.related_object_id = application.id
        self.related_object_type = 'Application'


class RepaymentReminderNotificationFactory(NotificationFactory):
    """
    Factory for repayment reminder notifications.
    """
    
    notification_type = 'repayment_reminder'
    title = 'Repayment Reminder'
    
    @factory.post_generation
    def repayment_reminder(self, create, extracted, **kwargs):
        if not create:
            return
            
        application = extracted if extracted else ApplicationFactory()
        self.message = f'Your repayment for application #{application.reference_number} is due soon.'
        self.related_object_id = application.id
        self.related_object_type = 'Application'


class RepaymentConfirmationNotificationFactory(NotificationFactory):
    """
    Factory for repayment confirmation notifications.
    """
    
    notification_type = 'repayment_confirmation'
    title = 'Repayment Confirmation'
    
    @factory.post_generation
    def repayment_confirmation(self, create, extracted, **kwargs):
        if not create:
            return
            
        application = extracted if extracted else ApplicationFactory()
        self.message = f'Your repayment for application #{application.reference_number} has been received.'
        self.related_object_id = application.id
        self.related_object_type = 'Application'


class RepaymentLateNotificationFactory(NotificationFactory):
    """
    Factory for repayment late notifications.
    """
    
    notification_type = 'repayment_late'
    title = 'Late Repayment'
    
    @factory.post_generation
    def repayment_late(self, create, extracted, **kwargs):
        if not create:
            return
            
        application = extracted if extracted else ApplicationFactory()
        self.message = f'Your repayment for application #{application.reference_number} is overdue.'
        self.related_object_id = application.id
        self.related_object_type = 'Application'


class SystemNotificationFactory(NotificationFactory):
    """
    Factory for system notifications.
    """
    
    notification_type = 'system'
    title = 'System Notification'
    message = factory.Faker('paragraph')
    # No related object for system notifications


class ReadNotificationFactory(NotificationFactory):
    """
    Factory for read notifications.
    """
    
    is_read = True
    
    @factory.post_generation
    def read_details(self, create, extracted, **kwargs):
        if create:
            # If the model has a read_at field, we would set it here
            pass


class UnreadNotificationFactory(NotificationFactory):
    """
    Factory for unread notifications.
    """
    
    is_read = False
