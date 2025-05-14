from django.urls import path
from .views import (
    RepaymentComplianceReportView,
    ApplicationVolumeReportView,
    ApplicationStatusReportView,
)

urlpatterns = [
    path('repayment-compliance/', RepaymentComplianceReportView.as_view(), name='repayment-compliance-report'),
    path('application-volume/', ApplicationVolumeReportView.as_view(), name='application-volume-report'),
    path('application-status/', ApplicationStatusReportView.as_view(), name='application-status-report'),
]
