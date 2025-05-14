from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from applications.models import Application
from users.models import User
from borrowers.models import Borrower
from documents.models import Document
import os
import tempfile
import datetime
import json

class DocumentAPITestCase(TestCase):
    def setUp(self):
        """
        Set up test data
        """
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        
        # Create test borrower
        self.borrower = Borrower.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            residential_address='123 Main St',
        )
        
        # Create test application
        self.application = Application.objects.create(
            reference_number='APP-2025-001',
            loan_amount=100000,
            loan_term=12,
            stage='inquiry',
            created_by=self.admin_user
        )
        self.application.borrowers.add(self.borrower)
        
        # Create test document
        self.test_file = SimpleUploadedFile(
            name='test_document.pdf',
            content=b'Test document content',
            content_type='application/pdf'
        )
        
        self.document = Document.objects.create(
            title='Test Document',
            description='Test document description',
            document_type='application_form',
            file=self.test_file,
            file_name='test_document.pdf',
            file_size=len(b'Test document content'),
            file_type='application/pdf',
            application=self.application,
            created_by=self.admin_user
        )
        
        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
    
    def tearDown(self):
        """
        Clean up after tests
        """
        # Delete test files
        for document in Document.objects.all():
            if document.file and os.path.isfile(document.file.path):
                os.remove(document.file.path)
    
    def test_document_list(self):
        """
        Test that admin can list all documents
        """
        url = reverse('document-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Document')
    
    def test_document_detail(self):
        """
        Test retrieving a document detail
        """
        url = reverse('document-detail', args=[self.document.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Document')
        self.assertEqual(response.data['document_type'], 'application_form')
    
    def test_document_create(self):
        """
        Test creating a new document
        """
        url = reverse('document-list')
        
        test_file = SimpleUploadedFile(
            name='new_document.pdf',
            content=b'New document content',
            content_type='application/pdf'
        )
        
        data = {
            'title': 'New Document',
            'description': 'New document description',
            'document_type': 'contract',
            'file': test_file,
            'application': self.application.id
        }
        
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 2)
        self.assertEqual(Document.objects.latest('id').title, 'New Document')
    
    def test_document_update(self):
        """
        Test updating a document
        """
        url = reverse('document-detail', args=[self.document.id])
        
        data = {
            'title': 'Updated Document',
            'description': 'Updated document description'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document.refresh_from_db()
        self.assertEqual(self.document.title, 'Updated Document')
        self.assertEqual(self.document.description, 'Updated document description')
    
    def test_document_delete(self):
        """
        Test deleting a document
        """
        url = reverse('document-detail', args=[self.document.id])
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Document.objects.count(), 0)
    
    def test_document_download(self):
        """
        Test downloading a document
        """
        url = reverse('document-download', args=[self.document.id])
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="{self.document.file_name}"')
        # FileResponse doesn't have content attribute, it has streaming_content
        content = b''.join(response.streaming_content)
        self.assertEqual(content, b'Test document content')
    
    def test_document_filtering(self):
        """
        Test document filtering
        """
        # Create another document with different type
        test_file2 = SimpleUploadedFile(
            name='contract.pdf',
            content=b'Contract content',
            content_type='application/pdf'
        )
        
        Document.objects.create(
            title='Contract Document',
            description='Contract document description',
            document_type='contract',
            file=test_file2,
            file_name='contract.pdf',
            file_size=len(b'Contract content'),
            file_type='application/pdf',
            application=self.application,
            created_by=self.admin_user
        )
        
        # Filter by document type
        url = reverse('document-list') + '?document_type=contract'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Contract Document')
        
        # Filter by application
        url = reverse('document-list') + f'?application={self.application.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_document_search(self):
        """
        Test document search
        """
        # Search by title
        url = reverse('document-list') + '?search=Test'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Document')


class DocumentVersionAPITestCase(TestCase):
    def setUp(self):
        """
        Set up test data
        """
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        
        # Create test application
        self.application = Application.objects.create(
            reference_number='APP-2025-002',
            loan_amount=200000,
            loan_term=24,
            stage='inquiry',
            created_by=self.admin_user
        )
        
        # Create test document
        self.test_file = SimpleUploadedFile(
            name='original_document.pdf',
            content=b'Original document content',
            content_type='application/pdf'
        )
        
        self.document = Document.objects.create(
            title='Original Document',
            description='Original document description',
            document_type='application_form',
            file=self.test_file,
            file_name='original_document.pdf',
            file_size=len(b'Original document content'),
            file_type='application/pdf',
            application=self.application,
            created_by=self.admin_user
        )
        
        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
    
    def tearDown(self):
        """
        Clean up after tests
        """
        # Delete test files
        for document in Document.objects.all():
            if document.file and os.path.isfile(document.file.path):
                os.remove(document.file.path)
    
    def test_create_document_version(self):
        """
        Test creating a new version of a document
        """
        url = reverse('document-create-version', args=[self.document.id])
        
        new_file = SimpleUploadedFile(
            name='new_version.pdf',
            content=b'New version content',
            content_type='application/pdf'
        )
        
        data = {
            'file': new_file,
            'description': 'Updated version description'
        }
        
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 2)
        
        # Check that the new version has the correct attributes
        new_version = Document.objects.latest('id')
        self.assertEqual(new_version.title, 'Original Document')
        self.assertEqual(new_version.description, 'Updated version description')
        self.assertEqual(new_version.document_type, 'application_form')
        self.assertEqual(new_version.version, 2)
        self.assertEqual(new_version.previous_version, self.document)
        self.assertEqual(new_version.application, self.application)
    
    def test_create_version_without_file(self):
        """
        Test creating a new version without providing a file
        """
        url = reverse('document-create-version', args=[self.document.id])
        
        data = {
            'description': 'Updated version description'
        }
        
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Document.objects.count(), 1)
    
    def test_create_version_nonexistent_document(self):
        """
        Test creating a new version for a nonexistent document
        """
        url = reverse('document-create-version', args=[9999])
        
        new_file = SimpleUploadedFile(
            name='new_version.pdf',
            content=b'New version content',
            content_type='application/pdf'
        )
        
        data = {
            'file': new_file,
            'description': 'Updated version description'
        }
        
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Document.objects.count(), 1)
    
    def test_multiple_versions(self):
        """
        Test creating multiple versions of a document
        """
        # Create version 2
        url = reverse('document-create-version', args=[self.document.id])
        
        file_v2 = SimpleUploadedFile(
            name='version2.pdf',
            content=b'Version 2 content',
            content_type='application/pdf'
        )
        
        data = {
            'file': file_v2,
            'description': 'Version 2 description'
        }
        
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get the version 2 document
        version2 = Document.objects.get(version=2)
        
        # Create version 3
        url = reverse('document-create-version', args=[version2.id])
        
        file_v3 = SimpleUploadedFile(
            name='version3.pdf',
            content=b'Version 3 content',
            content_type='application/pdf'
        )
        
        data = {
            'file': file_v3,
            'description': 'Version 3 description'
        }
        
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that we have 3 versions
        self.assertEqual(Document.objects.count(), 3)
        
        # Check version chain
        version3 = Document.objects.get(version=3)
        self.assertEqual(version3.previous_version, version2)
        self.assertEqual(version2.previous_version, self.document)
    
    def test_document_version_metadata(self):
        """
        Test that document version metadata is correctly maintained
        """
        # Create version 2
        url = reverse('document-create-version', args=[self.document.id])
        
        file_v2 = SimpleUploadedFile(
            name='version2.pdf',
            content=b'Version 2 content',
            content_type='application/pdf'
        )
        
        data = {
            'file': file_v2,
            'description': 'Version 2 description'
        }
        
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get the version 2 document
        version2 = Document.objects.get(version=2)
        
        # Check that metadata is preserved
        self.assertEqual(version2.title, self.document.title)
        self.assertEqual(version2.document_type, self.document.document_type)
        self.assertEqual(version2.application, self.document.application)
        
        # Check that file metadata is updated
        self.assertEqual(version2.file_name, 'version2.pdf')
        self.assertEqual(version2.file_size, len(b'Version 2 content'))
        self.assertEqual(version2.file_type, 'application/pdf')
        
        # Check that created_by is set to the current user
        self.assertEqual(version2.created_by, self.admin_user)
