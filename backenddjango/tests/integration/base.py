"""
Base classes for integration tests.
Focused on admin user testing with 100% API access.
"""

import json
import os
from typing import Dict, Any, List, Union, Optional
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


@override_settings(DJANGO_SETTINGS_MODULE='crm_backend.settings_integration')
class AdminIntegrationTestCase(TestCase):
    """
    Base class for admin integration tests.
    Provides common functionality for all integration tests with admin access.
    """
    
    def setUp(self):
        """
        Set up the test case with an admin user.
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin_test@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='Test',
            role='admin'
        )
        self.access_token = self.authenticate_as_admin()
    
    def authenticate_as_admin(self) -> str:
        """
        Authenticate the client as an admin user.
        
        Returns:
            str: The access token
        """
        refresh = RefreshToken.for_user(self.admin_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        return access_token
    
    def clear_authentication(self) -> None:
        """
        Clear the client's authentication credentials.
        """
        self.client.credentials()
    
    def refresh_authentication(self) -> str:
        """
        Refresh the admin authentication token.
        
        Returns:
            str: The new access token
        """
        self.clear_authentication()
        return self.authenticate_as_admin()
    
    # API Request Helpers
    
    def get_api(self, url_name: str, pk: int = None, query_params: Dict = None, 
                format: str = 'json', expected_status: int = status.HTTP_200_OK) -> Response:
        """
        Make a GET request to the API.
        
        Args:
            url_name: The name of the URL to reverse
            pk: Optional primary key for detail views
            query_params: Optional query parameters
            format: Response format (default: json)
            expected_status: Expected HTTP status code
            
        Returns:
            Response: The API response
        """
        url = reverse(url_name, args=[pk] if pk else None)
        if query_params:
            url += '?' + '&'.join([f"{k}={v}" for k, v in query_params.items()])
        
        response = self.client.get(url, format=format)
        self.assert_status_code(response, expected_status)
        return response
    
    def post_api(self, url_name: str, data: Dict, pk: int = None, 
                 format: str = 'json', expected_status: int = status.HTTP_201_CREATED) -> Response:
        """
        Make a POST request to the API.
        
        Args:
            url_name: The name of the URL to reverse
            data: The data to send
            pk: Optional primary key for detail views
            format: Request format (default: json)
            expected_status: Expected HTTP status code
            
        Returns:
            Response: The API response
        """
        url = reverse(url_name, args=[pk] if pk else None)
        response = self.client.post(url, data, format=format)
        self.assert_status_code(response, expected_status)
        return response
    
    def put_api(self, url_name: str, data: Dict, pk: int, 
                format: str = 'json', expected_status: int = status.HTTP_200_OK) -> Response:
        """
        Make a PUT request to the API.
        
        Args:
            url_name: The name of the URL to reverse
            data: The data to send
            pk: Primary key for the object to update
            format: Request format (default: json)
            expected_status: Expected HTTP status code
            
        Returns:
            Response: The API response
        """
        url = reverse(url_name, args=[pk])
        response = self.client.put(url, data, format=format)
        self.assert_status_code(response, expected_status)
        return response
    
    def patch_api(self, url_name: str, data: Dict, pk: int, 
                  format: str = 'json', expected_status: int = status.HTTP_200_OK) -> Response:
        """
        Make a PATCH request to the API.
        
        Args:
            url_name: The name of the URL to reverse
            data: The data to send
            pk: Primary key for the object to update
            format: Request format (default: json)
            expected_status: Expected HTTP status code
            
        Returns:
            Response: The API response
        """
        url = reverse(url_name, args=[pk])
        response = self.client.patch(url, data, format=format)
        self.assert_status_code(response, expected_status)
        return response
    
    def delete_api(self, url_name: str, pk: int, 
                   expected_status: int = status.HTTP_204_NO_CONTENT) -> Response:
        """
        Make a DELETE request to the API.
        
        Args:
            url_name: The name of the URL to reverse
            pk: Primary key for the object to delete
            expected_status: Expected HTTP status code
            
        Returns:
            Response: The API response
        """
        url = reverse(url_name, args=[pk])
        response = self.client.delete(url)
        self.assert_status_code(response, expected_status)
        return response
    
    def upload_file(self, url_name: str, file_path: str, file_field_name: str = 'file', 
                    data: Dict = None, pk: int = None, 
                    expected_status: int = status.HTTP_201_CREATED) -> Response:
        """
        Upload a file to the API.
        
        Args:
            url_name: The name of the URL to reverse
            file_path: Path to the file to upload
            file_field_name: Name of the file field
            data: Additional data to send
            pk: Optional primary key for detail views
            expected_status: Expected HTTP status code
            
        Returns:
            Response: The API response
        """
        url = reverse(url_name, args=[pk] if pk else None)
        
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        file_name = os.path.basename(file_path)
        uploaded_file = SimpleUploadedFile(
            name=file_name,
            content=file_content,
            content_type='application/octet-stream'
        )
        
        post_data = {file_field_name: uploaded_file}
        if data:
            post_data.update(data)
        
        response = self.client.post(url, post_data)
        self.assert_status_code(response, expected_status)
        return response
    
    # Assertion Helpers
    
    def assert_status_code(self, response: Response, expected_status: int) -> None:
        """
        Assert that the response has the expected status code.
        
        Args:
            response: The API response
            expected_status: Expected HTTP status code
        """
        self.assertEqual(
            response.status_code, 
            expected_status, 
            f"Expected status code {expected_status}, got {response.status_code}. Response: {response.content}"
        )
    
    def assert_response_contains(self, response: Response, key: str, value: Any = None) -> None:
        """
        Assert that the response contains the expected key and optionally value.
        
        Args:
            response: The API response
            key: The key to check for
            value: Optional value to check for
        """
        data = response.json()
        self.assertIn(key, data, f"Response does not contain key '{key}'. Response: {data}")
        if value is not None:
            self.assertEqual(data[key], value, f"Expected '{key}' to be '{value}', got '{data[key]}'")
    
    def assert_response_list_length(self, response: Response, expected_length: int) -> None:
        """
        Assert that the response contains a list of the expected length.
        
        Args:
            response: The API response
            expected_length: Expected length of the list
        """
        data = response.json()
        if 'results' in data:  # Paginated response
            actual_length = len(data['results'])
        else:  # Direct list response
            actual_length = len(data)
        
        self.assertEqual(
            actual_length, 
            expected_length, 
            f"Expected list of length {expected_length}, got {actual_length}. Response: {data}"
        )
    
    def assert_object_in_response(self, response: Response, field: str, value: Any) -> None:
        """
        Assert that the response contains an object with the given field and value.
        
        Args:
            response: The API response
            field: The field to check
            value: The value to check for
        """
        data = response.json()
        
        if 'results' in data:  # Paginated response
            objects = data['results']
        else:  # Direct list response
            objects = data
        
        found = False
        for obj in objects:
            if field in obj and obj[field] == value:
                found = True
                break
        
        self.assertTrue(found, f"No object found with {field}={value}. Response: {data}")
    
    def assert_object_count(self, model_class: Any, expected_count: int) -> None:
        """
        Assert that the number of objects of the given model class is as expected.
        
        Args:
            model_class: The model class to count objects for
            expected_count: Expected number of objects
        """
        actual_count = model_class.objects.count()
        self.assertEqual(
            actual_count, 
            expected_count, 
            f"Expected {expected_count} {model_class.__name__} objects, got {actual_count}"
        )
    
    def assert_object_exists(self, model_class: Any, **kwargs) -> None:
        """
        Assert that an object of the given model class exists with the given attributes.
        
        Args:
            model_class: The model class to check
            **kwargs: Attributes to filter by
        """
        self.assertTrue(
            model_class.objects.filter(**kwargs).exists(),
            f"No {model_class.__name__} found with attributes {kwargs}"
        )
    
    def assert_object_does_not_exist(self, model_class: Any, **kwargs) -> None:
        """
        Assert that no object of the given model class exists with the given attributes.
        
        Args:
            model_class: The model class to check
            **kwargs: Attributes to filter by
        """
        self.assertFalse(
            model_class.objects.filter(**kwargs).exists(),
            f"{model_class.__name__} found with attributes {kwargs} when it should not exist"
        )
    
    def assert_field_validation_error(self, response: Response, field_name: str) -> None:
        """
        Assert that the response contains a validation error for the given field.
        
        Args:
            response: The API response
            field_name: The field that should have a validation error
        """
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn(field_name, data, f"No validation error for field '{field_name}'. Response: {data}")
    
    def assert_permission_denied(self, response: Response) -> None:
        """
        Assert that the response indicates permission denied.
        
        Args:
            response: The API response
        """
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def assert_not_found(self, response: Response) -> None:
        """
        Assert that the response indicates not found.
        
        Args:
            response: The API response
        """
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # File Helpers
    
    def create_test_file(self, filename: str = 'test.txt', content: bytes = b'Test file content') -> SimpleUploadedFile:
        """
        Create a test file for upload tests.
        
        Args:
            filename: Name of the file
            content: Content of the file
            
        Returns:
            SimpleUploadedFile: The test file
        """
        return SimpleUploadedFile(
            name=filename,
            content=content,
            content_type='application/octet-stream'
        )
    
    def create_test_image(self, filename: str = 'test.jpg', size: tuple = (100, 100)) -> SimpleUploadedFile:
        """
        Create a test image for upload tests.
        
        Args:
            filename: Name of the image file
            size: Size of the image (width, height)
            
        Returns:
            SimpleUploadedFile: The test image
        """
        from PIL import Image
        import io
        
        image = Image.new('RGB', size, color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        
        return SimpleUploadedFile(
            name=filename,
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
    
    # Data Helpers
    
    def get_admin_headers(self) -> Dict[str, str]:
        """
        Get headers with admin authentication.
        
        Returns:
            Dict: Headers with admin authentication
        """
        refresh = RefreshToken.for_user(self.admin_user)
        return {'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}'}
