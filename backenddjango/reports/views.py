from django.db.models import Count, Sum, Avg, F, Q, Case, When, IntegerField, DecimalField, ExpressionWrapper, DateTimeField
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend

from applications.models import Application, Repayment
from brokers.models import BDM
from .serializers import (
    RepaymentComplianceReportSerializer,
    ApplicationVolumeReportSerializer,
    ApplicationStatusReportSerializer,
)


class RepaymentComplianceReportView(GenericAPIView):
    """
    API endpoint for repayment compliance reports
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RepaymentComplianceReportSerializer
    
    def get(self, request, format=None):
        # Get query parameters for filtering
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        application_id = request.query_params.get('application_id', None)
        
        # Base queryset
        repayments = Repayment.objects.all()
        
        # Apply filters
        if start_date:
            repayments = repayments.filter(due_date__gte=start_date)
        if end_date:
            repayments = repayments.filter(due_date__lte=end_date)
        if application_id:
            repayments = repayments.filter(application_id=application_id)
        
        # Calculate compliance metrics
        total_repayments = repayments.count()
        paid_on_time = repayments.filter(status='paid', paid_date__lte=F('due_date')).count()
        paid_late = repayments.filter(status='paid', paid_date__gt=F('due_date')).count()
        missed = repayments.filter(status='missed').count()
        
        # Calculate compliance rate
        compliance_rate = (paid_on_time / total_repayments * 100) if total_repayments > 0 else 0
        
        # Calculate average days late for late payments
        late_payments = repayments.filter(status='paid', paid_date__gt=F('due_date'))
        days_late = [
            (payment.paid_date - payment.due_date).days 
            for payment in late_payments 
            if payment.paid_date and payment.due_date
        ]
        average_days_late = sum(days_late) / len(days_late) if days_late else 0
        
        # Calculate total amounts
        total_amount_due = repayments.aggregate(total=Sum('amount'))['total'] or 0
        total_amount_paid = repayments.filter(status='paid').aggregate(total=Sum('payment_amount'))['total'] or 0
        payment_rate = (total_amount_paid / total_amount_due * 100) if total_amount_due > 0 else 0
        
        # Monthly breakdown
        monthly_data = repayments.annotate(
            month=TruncMonth('due_date')
        ).values('month').annotate(
            total=Count('id'),
            paid_on_time=Count(Case(
                When(status='paid', paid_date__lte=F('due_date'), then=1),
                output_field=IntegerField()
            )),
            paid_late=Count(Case(
                When(status='paid', paid_date__gt=F('due_date'), then=1),
                output_field=IntegerField()
            )),
            missed=Count(Case(
                When(status='missed', then=1),
                output_field=IntegerField()
            )),
            amount_due=Sum('amount'),
            amount_paid=Sum('payment_amount')
        ).order_by('month')
        
        monthly_breakdown = []
        for month_data in monthly_data:
            month_total = month_data['total']
            month_compliance = (month_data['paid_on_time'] / month_total * 100) if month_total > 0 else 0
            month_amount_due = month_data['amount_due'] or 0
            month_amount_paid = month_data['amount_paid'] or 0
            month_payment_rate = (month_amount_paid / month_amount_due * 100) if month_amount_due > 0 else 0
            
            monthly_breakdown.append({
                'month': month_data['month'].strftime('%Y-%m'),
                'total_repayments': month_total,
                'paid_on_time': month_data['paid_on_time'],
                'paid_late': month_data['paid_late'],
                'missed': month_data['missed'],
                'compliance_rate': round(month_compliance, 2),
                'amount_due': month_amount_due,
                'amount_paid': month_amount_paid,
                'payment_rate': round(month_payment_rate, 2)
            })
        
        # Prepare report data
        report_data = {
            'total_repayments': total_repayments,
            'paid_on_time': paid_on_time,
            'paid_late': paid_late,
            'missed': missed,
            'compliance_rate': round(compliance_rate, 2),
            'average_days_late': round(average_days_late, 2),
            'total_amount_due': total_amount_due,
            'total_amount_paid': total_amount_paid,
            'payment_rate': round(payment_rate, 2),
            'monthly_breakdown': monthly_breakdown
        }
        
        serializer = RepaymentComplianceReportSerializer(report_data)
        return Response(serializer.data)


class ApplicationVolumeReportView(GenericAPIView):
    """
    API endpoint for application volume reports
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationVolumeReportSerializer
    
    def get(self, request, format=None):
        # Get query parameters for filtering
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        bd_id = request.query_params.get('bd_id', None)
        broker_id = request.query_params.get('broker_id', None)
        time_grouping = request.query_params.get('time_grouping', 'month')  # day, week, month
        
        # Base queryset
        applications = Application.objects.all()
        
        # Apply filters
        if start_date:
            applications = applications.filter(created_at__gte=start_date)
        if end_date:
            applications = applications.filter(created_at__lte=end_date)
        if bd_id:
            applications = applications.filter(bd_id=bd_id)
        if broker_id:
            applications = applications.filter(broker_id=broker_id)
        
        # Calculate basic metrics
        total_applications = applications.count()
        total_loan_amount = applications.aggregate(total=Sum('loan_amount'))['total'] or 0
        average_loan_amount = applications.aggregate(avg=Avg('loan_amount'))['avg'] or 0
        
        # Breakdown by stage
        stage_breakdown = dict(applications.values_list('stage').annotate(count=Count('id')))
        
        # Breakdown by time period
        if time_grouping == 'day':
            time_function = TruncDay
            format_string = '%Y-%m-%d'
        elif time_grouping == 'week':
            time_function = TruncWeek
            format_string = '%Y-%m-%d'  # Week starting date
        else:  # Default to month
            time_function = TruncMonth
            format_string = '%Y-%m'
        
        time_data = applications.annotate(
            period=time_function('created_at')
        ).values('period').annotate(
            count=Count('id'),
            total_amount=Sum('loan_amount')
        ).order_by('period')
        
        time_breakdown = []
        for period_data in time_data:
            time_breakdown.append({
                'period': period_data['period'].strftime(format_string),
                'count': period_data['count'],
                'total_amount': period_data['total_amount'] or 0
            })
        
        # Breakdown by BD
        bd_data = applications.values('bd__id', 'bd__name').annotate(
            count=Count('id'),
            total_amount=Sum('loan_amount')
        ).order_by('-count')
        
        bd_breakdown = []
        for bd in bd_data:
            bd_breakdown.append({
                'bd_id': bd['bd__id'],
                'bd_name': bd['bd__name'] or 'No BD',
                'count': bd['count'],
                'total_amount': bd['total_amount'] or 0
            })
        
        # Breakdown by application type
        type_breakdown = dict(applications.values_list('application_type').annotate(count=Count('id')))
        
        # Prepare report data
        report_data = {
            'total_applications': total_applications,
            'total_loan_amount': total_loan_amount,
            'average_loan_amount': average_loan_amount,
            'stage_breakdown': stage_breakdown,
            'time_breakdown': time_breakdown,
            'bd_breakdown': bd_breakdown,
            'type_breakdown': type_breakdown
        }
        
        serializer = ApplicationVolumeReportSerializer(report_data)
        return Response(serializer.data)


class ApplicationStatusReportView(GenericAPIView):
    """
    API endpoint for application status reports
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationStatusReportSerializer
    
    def get(self, request, format=None):
        # Get query parameters for filtering
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        # Base queryset
        applications = Application.objects.all()
        
        # Apply filters
        if start_date:
            applications = applications.filter(created_at__gte=start_date)
        if end_date:
            applications = applications.filter(created_at__lte=end_date)
        
        # Calculate status metrics
        active_stages = [
            'inquiry', 'sent_to_lender', 'funding_table_issued', 'iloo_issued', 
            'iloo_signed', 'commitment_fee_paid', 'app_submitted', 'valuation_ordered', 
            'valuation_received', 'more_info_required', 'formal_approval', 'loan_docs_instructed', 
            'loan_docs_issued', 'loan_docs_signed', 'settlement_conditions'
        ]
        settled_stages = ['settled', 'closed']
        
        total_active = applications.filter(stage__in=active_stages).count()
        total_settled = applications.filter(stage__in=settled_stages).count()
        total_declined = applications.filter(stage='declined').count()
        total_withdrawn = applications.filter(stage='withdrawn').count()
        
        # Active applications by stage
        active_by_stage = {}
        for stage in active_stages:
            active_by_stage[stage] = applications.filter(stage=stage).count()
        
        # Calculate conversion rates
        total_inquiries = applications.filter(stage__in=['inquiry'] + active_stages[1:] + settled_stages + ['declined', 'withdrawn']).count()
        total_approvals = applications.filter(stage__in=['formal_approval'] + settled_stages + ['declined', 'withdrawn']).count()
        total_settlements = applications.filter(stage__in=settled_stages).count()
        
        inquiry_to_approval_rate = (total_approvals / total_inquiries * 100) if total_inquiries > 0 else 0
        approval_to_settlement_rate = (total_settlements / total_approvals * 100) if total_approvals > 0 else 0
        overall_success_rate = (total_settlements / total_inquiries * 100) if total_inquiries > 0 else 0
        
        # Prepare report data
        report_data = {
            'total_active': total_active,
            'total_settled': total_settled,
            'total_declined': total_declined,
            'total_withdrawn': total_withdrawn,
            'active_by_stage': active_by_stage,
            'avg_time_in_stage': {
                # This would require tracking stage changes over time
                # For now, we'll return placeholder values
                'inquiry': 0,
                'pre_approval': 0,
                'valuation': 0,
                'formal_approval': 0,
            },
            'inquiry_to_approval_rate': round(inquiry_to_approval_rate, 2),
            'approval_to_settlement_rate': round(approval_to_settlement_rate, 2),
            'overall_success_rate': round(overall_success_rate, 2)
        }
        
        serializer = ApplicationStatusReportSerializer(report_data)
        return Response(serializer.data)
