import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    """
    Filter for Product model
    """
    application = django_filters.NumberFilter(field_name='applications', lookup_expr='exact')
    borrower = django_filters.NumberFilter(field_name='borrowers', lookup_expr='exact')
    
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains'],
            'applications': ['exact'],
            'borrowers': ['exact'],
        }