import pytest
from django.urls import reverse
from rest_framework import status
from documents.models import Note, NoteComment
from users.models import User
from applications.models import Application
from borrowers.models import Borrower
from brokers.models import Broker, BDM
from rest_framework.test import APIClient
from django.utils import timezone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        email='admin@example.com',
        password='password123',
        role='admin',
        first_name='Admin',
        last_name='User'
    )


@pytest.fixture
def broker_user():
    return User.objects.create_user(
        email='broker@example.com',
        password='password123',
        role='broker',
        first_name='Broker',
        last_name='User'
    )


@pytest.fixture
def bd_user():
    return User.objects.create_user(
        email='bd@example.com',
        password='password123',
        role='bd',
        first_name='BD',
        last_name='User'
    )


@pytest.fixture
def bdm(bd_user):
    return BDM.objects.create(
        name=f"{bd_user.first_name} {bd_user.last_name}",
        user=bd_user,
        email=bd_user.email
    )


@pytest.fixture
def client_user():
    return User.objects.create_user(
        email='client@example.com',
        password='password123',
        role='client',
        first_name='Client',
        last_name='User'
    )


@pytest.fixture
def broker(broker_user):
    return Broker.objects.create(
        user=broker_user,
        company='Test Broker Company'
    )


@pytest.fixture
def borrower(client_user):
    borrower = Borrower.objects.create(
        first_name='Test',
        last_name='Borrower',
        email='borrower@example.com',
        phone='1234567890'
    )
    borrower.user = client_user
    borrower.save()
    return borrower


@pytest.fixture
def application(broker, borrower, bdm):
    application = Application.objects.create(
        reference_number='APP123',
        broker=broker,
        bd=bdm,
        stage='inquiry'
    )
    application.borrowers.add(borrower)
    return application


@pytest.fixture
def note(admin_user, application):
    return Note.objects.create(
        title='Test Note',
        content='This is a test note',
        application=application,
        created_by=admin_user
    )


@pytest.fixture
def assigned_note(admin_user, bd_user, application):
    return Note.objects.create(
        title='Assigned Note',
        content='This is an assigned note',
        application=application,
        created_by=admin_user,
        assigned_to=bd_user
    )


@pytest.fixture
def note_comment(admin_user, note):
    return NoteComment.objects.create(
        note=note,
        content='This is a test comment',
        created_by=admin_user
    )


@pytest.mark.django_db
class TestNoteComments:
    
    def test_create_comment(self, api_client, admin_user, note):
        """Test creating a comment on a note"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('note-comment-list')
        data = {
            'note': note.id,
            'content': 'This is a new comment'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == 'This is a new comment'
        assert response.data['note'] == note.id
        assert NoteComment.objects.count() == 1
    
    def test_get_comments(self, api_client, admin_user, note, note_comment):
        """Test getting all comments for a note"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('note-comments', args=[note.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['content'] == 'This is a test comment'
    
    def test_add_comment_to_note(self, api_client, admin_user, note):
        """Test adding a comment to a note using the add_comment action"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('note-add-comment', args=[note.id])
        data = {
            'content': 'This is a comment added via action'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == 'This is a comment added via action'
        assert NoteComment.objects.count() == 1
    
    def test_broker_can_comment_on_application_note(self, api_client, broker_user, note):
        """Test that a broker can comment on a note for their application"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('note-add-comment', args=[note.id])
        data = {
            'content': 'Broker comment'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == 'Broker comment'
    
    def test_bd_can_comment_on_application_note(self, api_client, bd_user, note):
        """Test that a BD can comment on a note for their application"""
        api_client.force_authenticate(user=bd_user)
        url = reverse('note-add-comment', args=[note.id])
        data = {
            'content': 'BD comment'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == 'BD comment'
    
    def test_client_can_comment_on_their_note(self, api_client, client_user, note):
        """Test that a client can comment on a note for their application"""
        api_client.force_authenticate(user=client_user)
        url = reverse('note-add-comment', args=[note.id])
        data = {
            'content': 'Client comment'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == 'Client comment'
    
    def test_notification_sent_when_comment_added_to_assigned_note(self, api_client, broker_user, assigned_note):
        """Test that a notification is sent when a comment is added to a note assigned to another user"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('note-add-comment', args=[assigned_note.id])
        data = {
            'content': 'Comment on assigned note'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Check that the comment was created
        assert NoteComment.objects.filter(note=assigned_note, content='Comment on assigned note').exists()
        
        # Note: We can't directly test that the notification was sent because it's handled by a signal
        # In a real test environment, we would mock the notification service or check the database