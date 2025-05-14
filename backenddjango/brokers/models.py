from django.db import models
from django.conf import settings


class Branch(models.Model):
    """
    Model for company branches
    """
    name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "branches"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class BDM(models.Model):
    """
    Model for Business Development Managers
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='branch_bdms')
    
    # User relationship
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bdm_profile')
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_bdms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "BDM"
        verbose_name_plural = "BDMs"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Broker(models.Model):
    """
    Model for brokers
    """
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    # Relationships
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='branch_brokers')
    bdms = models.ManyToManyField(BDM, related_name='bdm_brokers', blank=True)
    
    # User relationship
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='broker_profile')
    
    # Commission account information
    commission_bank_name = models.CharField(max_length=100, null=True, blank=True)
    commission_account_name = models.CharField(max_length=100, null=True, blank=True)
    commission_account_number = models.CharField(max_length=30, null=True, blank=True)
    commission_bsb = models.CharField(max_length=10, null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_brokers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.company})"
