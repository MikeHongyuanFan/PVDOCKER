from rest_framework import serializers
from .models import Broker, Branch, BDM
from users.serializers import UserSerializer


class BranchSerializer(serializers.ModelSerializer):
    """Serializer for branch information"""
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'phone', 'email']


class BDMSerializer(serializers.ModelSerializer):
    """Serializer for BDM information"""
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.IntegerField(write_only=True, required=False)
    
    # Branch address fields (write-only)
    branch_name = serializers.CharField(write_only=True, required=False)
    address = serializers.CharField(write_only=True, required=False)
    branch_phone = serializers.CharField(write_only=True, required=False)
    branch_email = serializers.EmailField(write_only=True, required=False)
    
    class Meta:
        model = BDM
        fields = ['id', 'name', 'email', 'phone', 'branch', 'branch_id', 
                 'branch_name', 'address', 'branch_phone', 'branch_email']
    
    def create(self, validated_data):
        branch_id = validated_data.pop('branch_id', None)
        branch_name = validated_data.pop('branch_name', None)
        address = validated_data.pop('address', None)
        branch_phone = validated_data.pop('branch_phone', None)
        branch_email = validated_data.pop('branch_email', None)
        
        # Handle branch association
        branch = None
        if branch_id:
            # Use existing branch if branch_id is provided
            try:
                branch = Branch.objects.get(id=branch_id)
            except Branch.DoesNotExist:
                raise serializers.ValidationError({"branch_id": "Branch with this ID does not exist"})
        elif branch_name:
            # Create new branch if branch_name is provided
            branch = Branch.objects.create(
                name=branch_name,
                address=address,
                phone=branch_phone,
                email=branch_email,
                created_by=validated_data.get('created_by')
            )
        
        # Create BDM instance
        bdm = BDM.objects.create(branch=branch, **validated_data)
        return bdm
        
    def update(self, instance, validated_data):
        branch_id = validated_data.pop('branch_id', None)
        branch_name = validated_data.pop('branch_name', None)
        address = validated_data.pop('address', None)
        branch_phone = validated_data.pop('branch_phone', None)
        branch_email = validated_data.pop('branch_email', None)
        
        # Handle branch association
        if branch_id:
            # Use existing branch if branch_id is provided
            try:
                branch = Branch.objects.get(id=branch_id)
                instance.branch = branch
            except Branch.DoesNotExist:
                raise serializers.ValidationError({"branch_id": "Branch with this ID does not exist"})
        elif branch_name and not instance.branch:
            # Create new branch if branch_name is provided and BDM doesn't have a branch
            branch = Branch.objects.create(
                name=branch_name,
                address=address,
                phone=branch_phone,
                email=branch_email,
                created_by=validated_data.get('created_by', instance.created_by)
            )
            instance.branch = branch
        elif instance.branch and (address or branch_phone or branch_email):
            # Update existing branch if BDM already has one
            if address:
                instance.branch.address = address
            if branch_phone:
                instance.branch.phone = branch_phone
            if branch_email:
                instance.branch.email = branch_email
            instance.branch.save()
        
        # Update BDM fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BrokerListSerializer(serializers.ModelSerializer):
    """Serializer for listing brokers with minimal information"""
    class Meta:
        model = Broker
        fields = ['id', 'name', 'company', 'email', 'phone']


class BrokerDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed broker information"""
    branch = BranchSerializer(read_only=True)
    bdms = BDMSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Broker
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
