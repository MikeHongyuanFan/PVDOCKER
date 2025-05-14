from rest_framework import serializers


class RepaymentComplianceReportSerializer(serializers.Serializer):
    """
    Serializer for repayment compliance report data
    """
    total_repayments = serializers.IntegerField()
    paid_on_time = serializers.IntegerField()
    paid_late = serializers.IntegerField()
    missed = serializers.IntegerField()
    compliance_rate = serializers.FloatField()
    average_days_late = serializers.FloatField()
    total_amount_due = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_amount_paid = serializers.DecimalField(max_digits=12, decimal_places=2)
    payment_rate = serializers.FloatField()
    
    # Breakdown by month
    monthly_breakdown = serializers.ListField(child=serializers.DictField())


class ApplicationVolumeReportSerializer(serializers.Serializer):
    """
    Serializer for application volume report data
    """
    total_applications = serializers.IntegerField()
    total_loan_amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    average_loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    # Breakdown by stage
    stage_breakdown = serializers.DictField(child=serializers.IntegerField())
    
    # Breakdown by time period (day, week, month)
    time_breakdown = serializers.ListField(child=serializers.DictField())
    
    # Breakdown by BD
    bd_breakdown = serializers.ListField(child=serializers.DictField())
    
    # Breakdown by application type
    type_breakdown = serializers.DictField(child=serializers.IntegerField())


class ApplicationStatusReportSerializer(serializers.Serializer):
    """
    Serializer for application status report data
    """
    total_active = serializers.IntegerField()
    total_settled = serializers.IntegerField()
    total_declined = serializers.IntegerField()
    total_withdrawn = serializers.IntegerField()
    
    # Active applications by stage
    active_by_stage = serializers.DictField(child=serializers.IntegerField())
    
    # Average time in each stage (days)
    avg_time_in_stage = serializers.DictField(child=serializers.FloatField())
    
    # Conversion rates
    inquiry_to_approval_rate = serializers.FloatField()
    approval_to_settlement_rate = serializers.FloatField()
    overall_success_rate = serializers.FloatField()
