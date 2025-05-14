"""
Factory for Document model.
"""

import factory
import random
from factory.django import DjangoModelFactory
from documents.models import Document
from .application_factory import ApplicationFactory
from .borrower_factory import BorrowerFactory
from .user_factory import UserFactory


class DocumentFactory(DjangoModelFactory):
    """
    Base factory for Document model.
    """
    
    class Meta:
        model = Document
    
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph')
    document_type = factory.Iterator(['ID', 'Income', 'Property', 'Insurance', 'Tax', 'Other'])
    file = factory.django.FileField(filename='test_document.pdf')
    file_name = factory.LazyAttribute(lambda obj: obj.file.name if obj.file else 'test_document.pdf')
    file_size = factory.LazyFunction(lambda: random.randint(1024, 10485760))  # 1KB to 10MB
    file_type = 'application/pdf'
    version = 1
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at)
    
    @factory.post_generation
    def application(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            self.application = extracted
        else:
            # Create a default application if none provided
            self.application = ApplicationFactory()
    
    @factory.post_generation
    def borrower(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            self.borrower = extracted
        else:
            # Create a default borrower if none provided
            self.borrower = BorrowerFactory()


class IDDocumentFactory(DocumentFactory):
    """
    Factory for ID documents.
    """
    
    document_type = 'ID'
    title = factory.Iterator(['Driver License', 'Passport', 'State ID', 'Military ID'])
    file = factory.django.FileField(filename='id_document.pdf')
    file_name = factory.LazyAttribute(lambda obj: obj.file.name if obj.file else 'id_document.pdf')


class IncomeDocumentFactory(DocumentFactory):
    """
    Factory for income documents.
    """
    
    document_type = 'Income'
    title = factory.Iterator(['Pay Stub', 'W-2', 'Tax Return', 'Employment Verification', 'Bank Statement'])
    file = factory.django.FileField(filename='income_document.pdf')
    file_name = factory.LazyAttribute(lambda obj: obj.file.name if obj.file else 'income_document.pdf')


class PropertyDocumentFactory(DocumentFactory):
    """
    Factory for property documents.
    """
    
    document_type = 'Property'
    title = factory.Iterator(['Property Appraisal', 'Title Report', 'Purchase Agreement', 'Property Insurance', 'Deed'])
    file = factory.django.FileField(filename='property_document.pdf')
    file_name = factory.LazyAttribute(lambda obj: obj.file.name if obj.file else 'property_document.pdf')


class InsuranceDocumentFactory(DocumentFactory):
    """
    Factory for insurance documents.
    """
    
    document_type = 'Insurance'
    title = factory.Iterator(['Homeowner Insurance', 'Flood Insurance', 'Title Insurance', 'Mortgage Insurance'])
    file = factory.django.FileField(filename='insurance_document.pdf')
    file_name = factory.LazyAttribute(lambda obj: obj.file.name if obj.file else 'insurance_document.pdf')


class TaxDocumentFactory(DocumentFactory):
    """
    Factory for tax documents.
    """
    
    document_type = 'Tax'
    title = factory.Iterator(['Tax Return', 'Property Tax Statement', 'Tax Transcript', 'W-2'])
    file = factory.django.FileField(filename='tax_document.pdf')
    file_name = factory.LazyAttribute(lambda obj: obj.file.name if obj.file else 'tax_document.pdf')


class VersionedDocumentFactory(DocumentFactory):
    """
    Factory for versioned documents.
    """
    
    version = factory.Sequence(lambda n: n + 1)
    
    @factory.post_generation
    def previous_version(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            self.previous_version = extracted
        elif self.version > 1:
            # Create a previous version if this is not version 1
            prev_version = DocumentFactory(
                title=self.title,
                document_type=self.document_type,
                application=self.application,
                borrower=self.borrower,
                version=self.version - 1
            )
            self.previous_version = prev_version
