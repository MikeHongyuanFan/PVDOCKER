from django.db import models
from django.conf import settings
from applications.models import Application
from documents.models import Document
from borrowers.models import Borrower


class Product(models.Model):
    """
    Model for loan products
    """
    # Basic product information
    name = models.CharField(max_length=255)
    
    # Relationships
    applications = models.ManyToManyField(Application, related_name="products")
    documents = models.ManyToManyField(Document, related_name="products")
    borrowers = models.ManyToManyField(Borrower, related_name="products")
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.name