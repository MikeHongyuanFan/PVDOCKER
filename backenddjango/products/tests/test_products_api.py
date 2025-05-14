from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import Product
from applications.models import Application
from borrowers.models import Borrower
import pytest

User = get_user_model()


@pytest.mark.django_db
class ProductAPITests(APITestCase):
    """
    Test suite for the Product API
    """
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            created_by=self.user
        )
        
        # URLs
        self.products_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', args=[self.product.id])
    
    def test_create_product(self):
        """Test creating a new product"""
        data = {'name': 'New Test Product'}
        response = self.client.post(self.products_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(id=response.data['id']).name, 'New Test Product')
    
    def test_get_products_list(self):
        """Test retrieving a list of products"""
        # Clear any existing products that might be in the database
        Product.objects.all().delete()
        
        # Create our test product again
        self.product = Product.objects.create(
            name='Test Product',
            created_by=self.user
        )
        
        response = self.client.get(self.products_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response is paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)  # Should be 1 product in the list
        else:
            self.assertEqual(len(response.data), 1)  # Should be 1 product in the list
    
    def test_get_product_detail(self):
        """Test retrieving a specific product"""
        response = self.client.get(self.product_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')
    
    def test_update_product(self):
        """Test updating a product"""
        data = {'name': 'Updated Test Product'}
        response = self.client.patch(self.product_detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Test Product')
    
    def test_delete_product(self):
        """Test deleting a product"""
        response = self.client.delete(self.product_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
    
    def test_product_application_relationship(self):
        """Test the many-to-many relationship between products and applications"""
        # Create a test application
        application = Application.objects.create(
            reference_number='TEST-12345',
            stage='inquiry',
            created_by=self.user
        )
        
        # Add the application to the product
        self.product.applications.add(application)
        
        # Check that the relationship is established
        self.assertEqual(self.product.applications.count(), 1)
        self.assertEqual(application.products.count(), 1)
        
        # Check that the application is in the product's applications
        self.assertIn(application, self.product.applications.all())
        
        # Check that the product is in the application's products
        self.assertIn(self.product, application.products.all())
    
    def test_product_borrower_relationship(self):
        """Test the many-to-many relationship between products and borrowers"""
        # Create a test borrower
        borrower = Borrower.objects.create(
            first_name='Test',
            last_name='Borrower',
            created_by=self.user
        )
        
        # Add the borrower to the product
        self.product.borrowers.add(borrower)
        
        # Check that the relationship is established
        self.assertEqual(self.product.borrowers.count(), 1)
        self.assertEqual(borrower.products.count(), 1)
        
        # Check that the borrower is in the product's borrowers
        self.assertIn(borrower, self.product.borrowers.all())
        
        # Check that the product is in the borrower's products
        self.assertIn(self.product, borrower.products.all())
