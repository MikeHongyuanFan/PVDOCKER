from rest_framework import serializers
from .models import Borrower, Guarantor
from users.serializers import UserSerializer
from drf_spectacular.utils import extend_schema_serializer


class BorrowerListSerializer(serializers.ModelSerializer):
    """Serializer for listing borrowers with minimal information"""
    application_count = serializers.SerializerMethodField()
    related_brokers = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'first_name', 'last_name', 'email', 
            'phone', 'created_at', 'application_count',
            'residential_address', 'mailing_address', 'address',
            'related_brokers', 'is_company'
        ]
    
    def get_application_count(self, obj) -> int:
        return obj.borrower_applications.count()
        
    def get_related_brokers(self, obj) -> list:
        """Get brokers related to this borrower through applications"""
        from brokers.serializers import BrokerListSerializer
        from brokers.models import Broker
        
        # Get unique broker IDs from all applications this borrower is associated with
        broker_ids = obj.borrower_applications.values_list('broker_id', flat=True).distinct()
        
        # Filter out None values
        broker_ids = [bid for bid in broker_ids if bid is not None]
        
        if not broker_ids:
            return []
            
        # Get the broker objects
        brokers = Broker.objects.filter(id__in=broker_ids)
        
        # Serialize the brokers
        return BrokerListSerializer(brokers, many=True).data
        
    def get_address(self, obj) -> dict:
        """Get formatted address information"""
        if obj.is_company:
            # Return company address information
            return {
                'unit': obj.registered_address_unit,
                'street_no': obj.registered_address_street_no,
                'street_name': obj.registered_address_street_name,
                'suburb': obj.registered_address_suburb,
                'state': obj.registered_address_state,
                'postcode': obj.registered_address_postcode,
                'full_address': obj.company_address or '',
            }
        else:
            # Return individual address information
            return {
                'residential_address': obj.residential_address or '',
                'mailing_address': obj.mailing_address or '',
            }


class BorrowerDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed borrower information"""
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Borrower
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class BorrowerFinancialSummarySerializer(serializers.Serializer):
    """Serializer for borrower financial summary"""
    total_applications = serializers.IntegerField()
    total_funded = serializers.DecimalField(max_digits=15, decimal_places=2)
    active_loans = serializers.IntegerField()
    active_loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    completed_loans = serializers.IntegerField()
    completed_loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2)


from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(component_name="BorrowerGuarantor")
class GuarantorSerializer(serializers.ModelSerializer):
    """Serializer for guarantor information"""
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Guarantor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)
    
    def validate(self, data):
        """
        Validate that the appropriate fields are provided based on guarantor type
        """
        guarantor_type = data.get('guarantor_type')
        
        if guarantor_type == 'individual':
            if not data.get('first_name') or not data.get('last_name'):
                raise serializers.ValidationError("First name and last name are required for individual guarantors")
        elif guarantor_type == 'company':
            if not data.get('company_name'):
                raise serializers.ValidationError("Company name is required for company guarantors")
        
        return data
