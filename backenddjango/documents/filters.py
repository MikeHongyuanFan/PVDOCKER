import django_filters
from django.db.models import Q
from .models import Document, Note, Fee, Repayment, NoteComment


class DocumentFilter(django_filters.FilterSet):
    """
    Custom filter for documents with advanced filtering options
    """
    search = django_filters.CharFilter(method='search_filter')
    created_after = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')
    
    class Meta:
        model = Document
        fields = [
            'document_type', 'application', 'borrower', 'search',
            'created_after', 'created_before'
        ]
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(file_name__icontains=value)
        )


class NoteFilter(django_filters.FilterSet):
    """
    Custom filter for notes with advanced filtering options
    """
    search = django_filters.CharFilter(method='search_filter')
    created_after = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')
    
    class Meta:
        model = Note
        fields = [
            'application', 'borrower', 'search',
            'created_after', 'created_before'
        ]
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(title__icontains=value) |
            Q(content__icontains=value)
        )


class FeeFilter(django_filters.FilterSet):
    """
    Custom filter for fees with advanced filtering options
    """
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='lte')
    due_after = django_filters.DateFilter(field_name="due_date", lookup_expr='gte')
    due_before = django_filters.DateFilter(field_name="due_date", lookup_expr='lte')
    is_paid = django_filters.BooleanFilter(field_name="paid_date", lookup_expr='isnull', exclude=True)
    
    class Meta:
        model = Fee
        fields = [
            'fee_type', 'application', 'min_amount', 'max_amount',
            'due_after', 'due_before', 'is_paid'
        ]


class RepaymentFilter(django_filters.FilterSet):
    """
    Custom filter for repayments with advanced filtering options
    """
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='lte')
    due_after = django_filters.DateFilter(field_name="due_date", lookup_expr='gte')
    due_before = django_filters.DateFilter(field_name="due_date", lookup_expr='lte')
    is_paid = django_filters.BooleanFilter(field_name="paid_date", lookup_expr='isnull', exclude=True)
    
    class Meta:
        model = Repayment
        fields = [
            'application', 'min_amount', 'max_amount',
            'due_after', 'due_before', 'is_paid'
        ]


class NoteCommentFilter(django_filters.FilterSet):
    """
    Custom filter for note comments with advanced filtering options
    """
    search = django_filters.CharFilter(method='search_filter')
    created_after = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')
    
    class Meta:
        model = NoteComment
        fields = [
            'note', 'created_by', 'search',
            'created_after', 'created_before'
        ]
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(content__icontains=value)
        )
