import django_filters
from django.db.models import Q, Count
from .models import Broker, Branch, BDM


class BrokerFilter(django_filters.FilterSet):
    """
    Custom filter for brokers with advanced filtering options
    """
    search = django_filters.CharFilter(method='search_filter')
    min_applications = django_filters.NumberFilter(method='filter_min_applications')
    
    class Meta:
        model = Broker
        fields = ['branch', 'search', 'min_applications']
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(name__icontains=value) |
            Q(company__icontains=value) |
            Q(email__icontains=value) |
            Q(phone__icontains=value)
        )
    
    def filter_min_applications(self, queryset, name, value):
        """
        Filter brokers with at least a certain number of applications
        """
        return queryset.annotate(
            application_count=Count('applications')
        ).filter(application_count__gte=value)


class BranchFilter(django_filters.FilterSet):
    """
    Custom filter for branches with advanced filtering options
    """
    search = django_filters.CharFilter(method='search_filter')
    
    class Meta:
        model = Branch
        fields = ['search']
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(name__icontains=value) |
            Q(address__icontains=value)
        )


class BDMFilter(django_filters.FilterSet):
    """
    Custom filter for BDMs with advanced filtering options
    """
    search = django_filters.CharFilter(method='search_filter')
    
    class Meta:
        model = BDM
        fields = ['branch', 'search']
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone__icontains=value)
        )
