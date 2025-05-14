from rest_framework import serializers
from .models import Document, Note, Fee, Repayment, Ledger, NoteComment


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for documents
    """
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    created_by_name = serializers.StringRelatedField(source='created_by')
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['file_name', 'file_size', 'file_type', 'version', 'created_by', 'created_at', 'updated_at']
    
    def get_file_url(self, obj) -> str:
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None


class NoteCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for note comments
    """
    created_by_name = serializers.StringRelatedField(source='created_by')
    
    class Meta:
        model = NoteComment
        fields = ['id', 'note', 'content', 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for notes
    """
    created_by_name = serializers.StringRelatedField(source='created_by')
    assigned_to_name = serializers.StringRelatedField(source='assigned_to')
    comments = NoteCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class FeeSerializer(serializers.ModelSerializer):
    """
    Serializer for fees
    """
    fee_type_display = serializers.CharField(source='get_fee_type_display', read_only=True)
    created_by_name = serializers.StringRelatedField(source='created_by')
    status = serializers.SerializerMethodField()
    invoice_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Fee
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def get_status(self, obj) -> str:
        if obj.paid_date:
            return 'paid'
        return 'pending'
    
    def get_invoice_url(self, obj) -> str:
        if obj.invoice:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.invoice.url)
        return None


class RepaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for repayments
    """
    created_by_name = serializers.StringRelatedField(source='created_by')
    status = serializers.SerializerMethodField()
    invoice_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Repayment
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'reminder_sent', 'overdue_3_day_sent', 'overdue_7_day_sent', 'overdue_10_day_sent']
    
    def get_status(self, obj) -> str:
        if obj.paid_date:
            return 'paid'
        
        from datetime import date
        today = date.today()
        
        if obj.due_date and obj.due_date < today:
            days_overdue = (today - obj.due_date).days
            return f'overdue_{days_overdue}_days'
        
        if obj.due_date:
            days_until_due = (obj.due_date - today).days
            if days_until_due <= 7:
                return f'due_soon_{days_until_due}_days'
        
        return 'scheduled'
    
    def get_invoice_url(self, obj) -> str:
        if obj.invoice:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.invoice.url)
        return None


class LedgerSerializer(serializers.ModelSerializer):
    """
    Serializer for ledger entries
    """
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    related_fee_type = serializers.CharField(source='related_fee.get_fee_type_display', read_only=True)
    created_by_name = serializers.StringRelatedField(source='created_by')
    
    class Meta:
        model = Ledger
        fields = [
            'id', 'application', 'transaction_type', 'transaction_type_display',
            'amount', 'description', 'transaction_date', 'related_fee',
            'related_fee_type', 'related_repayment', 'created_by', 'created_by_name', 'created_at'
        ]


class ApplicationLedgerSerializer(serializers.Serializer):
    """
    Serializer for application ledger summary
    """
    ledger_entries = LedgerSerializer(many=True)
    total_funded = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_repaid = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_fees = serializers.DecimalField(max_digits=15, decimal_places=2)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2)