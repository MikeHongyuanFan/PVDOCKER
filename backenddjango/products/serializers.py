from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'applications', 'documents', 'borrowers', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'applications': {'required': False},
            'documents': {'required': False},
            'borrowers': {'required': False},
        }