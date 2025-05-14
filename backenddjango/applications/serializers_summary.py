class SolvencyEnquiriesSerializer(serializers.Serializer):
    """
    Serializer for solvency enquiries summary
    """
    has_solvency_issues = serializers.BooleanField(read_only=True)
    solvency_issues_count = serializers.IntegerField(read_only=True)
    solvency_issues_summary = serializers.CharField(read_only=True)
    
    def to_representation(self, instance):
        # Count how many solvency issues are marked as True
        solvency_fields = [
            'has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
            'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
            'has_payment_arrangements'
        ]
        
        issues_count = sum(1 for field in solvency_fields if getattr(instance, field, False))
        has_issues = issues_count > 0
        
        # Create a summary of the issues
        issues_summary = []
        if instance.has_pending_litigation:
            issues_summary.append("Has pending/past litigation")
        if instance.has_unsatisfied_judgements:
            issues_summary.append("Has unsatisfied judgements")
        if instance.has_been_bankrupt:
            issues_summary.append("Has bankruptcy history")
        if instance.has_been_refused_credit:
            issues_summary.append("Has been refused credit")
        if instance.has_outstanding_ato_debt:
            issues_summary.append("Has outstanding ATO debt")
        if instance.has_outstanding_tax_returns:
            issues_summary.append("Has outstanding tax returns")
        if instance.has_payment_arrangements:
            issues_summary.append("Has payment arrangements")
        
        summary = ", ".join(issues_summary) if issues_summary else "No solvency issues"
        
        return {
            'has_solvency_issues': has_issues,
            'solvency_issues_count': issues_count,
            'solvency_issues_summary': summary
        }
