import django_filters
from django.db.models import Q
from .models import Borrower, Guarantor


class BorrowerFilter(django_filters.FilterSet):
    """
    Custom filter for borrowers with advanced filtering options
    """
    search = django_filters.CharFilter(method='search_filter')
    has_applications = django_filters.BooleanFilter(method='filter_has_applications')
    
    class Meta:
        model = Borrower
        fields = [
            'residency_status', 'marital_status', 'search', 'has_applications'
        ]
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone__icontains=value) |
            Q(residential_address__icontains=value)
        )
    
    def filter_has_applications(self, queryset, name, value):
        """
        Filter borrowers with or without applications
        """
        if value:
            return queryset.filter(applications__isnull=False).distinct()
        return queryset.filter(applications__isnull=True)


class GuarantorFilter(django_filters.FilterSet):
    """
    Custom filter for guarantors with advanced filtering options
    """
    search = django_filters.CharFilter(method='search_filter')
    
    class Meta:
        model = Guarantor
        fields = [
            'guarantor_type', 'borrower', 'application', 'search'
        ]
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone__icontains=value) |
            Q(company_name__icontains=value) |
            Q(address__icontains=value)
        )
