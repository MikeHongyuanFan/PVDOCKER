from rest_framework import serializers
from borrowers.models import Asset
from drf_spectacular.utils import extend_schema_field
from rest_framework.serializers import ListSerializer

class GuarantorAssetSerializer(serializers.ModelSerializer):
    """
    Serializer for guarantor assets
    """
    class Meta:
        model = Asset
        fields = ['id', 'asset_type', 'description', 'value', 'amount_owing', 'address', 'bg_type']
        
    def validate(self, data):
        """
        Validate that bg_type is provided and to_be_refinanced is not
        """
        if 'bg_type' not in data or not data['bg_type']:
            raise serializers.ValidationError({"bg_type": "bg_type is required for guarantor assets"})
        
        # Ensure to_be_refinanced is not set for guarantor assets
        data['to_be_refinanced'] = False
        
        return data


class CompanyAssetSerializer(serializers.ModelSerializer):
    """
    Serializer for company assets
    """
    class Meta:
        model = Asset
        fields = ['id', 'asset_type', 'description', 'value', 'amount_owing', 'to_be_refinanced', 'address']
        
    def validate(self, data):
        """
        Validate that bg_type is not provided
        """
        # Ensure bg_type is not set for company assets
        data['bg_type'] = None
        
        return data
