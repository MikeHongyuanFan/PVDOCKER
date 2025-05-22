from django_filters import FilterSet, NumberFilter, DateFilter, CharFilter, ChoiceFilter, BooleanFilter
from django.db.models import Q
from .models import Application


class ApplicationFilter(FilterSet):
    """
    Enhanced filter for applications with comprehensive filtering options
    """
    # Existing filters
    min_loan_amount = NumberFilter(field_name="loan_amount", lookup_expr='gte')
    max_loan_amount = NumberFilter(field_name="loan_amount", lookup_expr='lte')
    min_interest_rate = NumberFilter(field_name="interest_rate", lookup_expr='gte')
    max_interest_rate = NumberFilter(field_name="interest_rate", lookup_expr='lte')
    created_after = DateFilter(field_name="created_at", lookup_expr='gte')
    created_before = DateFilter(field_name="created_at", lookup_expr='lte')
    search = CharFilter(method='search_filter')
    stage = ChoiceFilter(choices=Application.STAGE_CHOICES)
    reference_number = CharFilter(lookup_expr='icontains')
    
    # New filters
    borrower_name = CharFilter(method='borrower_name_filter')
    guarantor_name = CharFilter(method='guarantor_name_filter')
    purpose = CharFilter(field_name='purpose', lookup_expr='icontains')
    loan_purpose = CharFilter(field_name='loan_purpose', lookup_expr='icontains')
    has_solvency_issues = BooleanFilter(method='solvency_issues_filter')
    estimated_settlement_date_after = DateFilter(field_name="estimated_settlement_date", lookup_expr='gte')
    estimated_settlement_date_before = DateFilter(field_name="estimated_settlement_date", lookup_expr='lte')
    is_signed = BooleanFilter(method='signed_filter')
    security_address = CharFilter(method='security_address_filter')
    application_type = ChoiceFilter(choices=Application.APPLICATION_TYPE_CHOICES)
    
    class Meta:
        model = Application
        fields = [
            'stage', 'application_type', 'broker', 'bd', 'bd_id', 'branch', 'branch_id',
            'min_loan_amount', 'max_loan_amount', 'min_interest_rate', 
            'max_interest_rate', 'created_after', 'created_before',
            'repayment_frequency', 'reference_number', 'borrower_name',
            'guarantor_name', 'purpose', 'loan_purpose', 'has_solvency_issues',
            'estimated_settlement_date_after', 'estimated_settlement_date_before', 'is_signed',
            'security_address', 'application_type'
        ]
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(reference_number__icontains=value) |
            Q(purpose__icontains=value) |
            Q(loan_purpose__icontains=value) |
            Q(borrowers__first_name__icontains=value) |
            Q(borrowers__last_name__icontains=value) |
            Q(borrowers__email__icontains=value) |
            Q(borrowers__company_name__icontains=value) |
            Q(guarantors__first_name__icontains=value) |
            Q(guarantors__last_name__icontains=value) |
            Q(security_address__icontains=value)
        ).distinct()
    
    def borrower_name_filter(self, queryset, name, value):
        """
        Filter by borrower name (first name, last name, or company name)
        """
        return queryset.filter(
            Q(borrowers__first_name__icontains=value) |
            Q(borrowers__last_name__icontains=value) |
            Q(borrowers__company_name__icontains=value)
        ).distinct()
    
    def guarantor_name_filter(self, queryset, name, value):
        """
        Filter by guarantor name
        """
        return queryset.filter(
            Q(guarantors__first_name__icontains=value) |
            Q(guarantors__last_name__icontains=value)
        ).distinct()
    
    def solvency_issues_filter(self, queryset, name, value):
        """
        Filter applications with solvency issues
        """
        if value:
            return queryset.filter(
                Q(has_pending_litigation=True) |
                Q(has_unsatisfied_judgements=True) |
                Q(has_been_bankrupt=True) |
                Q(has_been_refused_credit=True) |
                Q(has_outstanding_ato_debt=True) |
                Q(has_outstanding_tax_returns=True) |
                Q(has_payment_arrangements=True)
            )
        return queryset
    
    def signed_filter(self, queryset, name, value):
        """
        Filter by signed status
        """
        if value:
            return queryset.exclude(signed_by__isnull=True).exclude(signed_by='')
        else:
            return queryset.filter(Q(signed_by__isnull=True) | Q(signed_by=''))
    
    def security_address_filter(self, queryset, name, value):
        """
        Filter by security property address
        """
        return queryset.filter(
            Q(security_address__icontains=value) |
            Q(securityproperty_set__address_street_name__icontains=value) |
            Q(securityproperty_set__address_suburb__icontains=value) |
            Q(securityproperty_set__address_state__icontains=value) |
            Q(securityproperty_set__address_postcode__icontains=value)
        ).distinct()
