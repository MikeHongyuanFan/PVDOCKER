"""
URL patterns for asynchronous task endpoints.
"""

from django.urls import path
from .task_views import (
    generate_document_async_view,
    generate_pdf_async_view,
    calculate_funding_async_view,
    task_status_view,
    task_result_view
)

urlpatterns = [
    # Asynchronous task endpoints
    path('documents/generate-async/<int:application_id>/', generate_document_async_view, name='generate-document-async'),
    path('documents/generate-pdf-async/<int:application_id>/', generate_pdf_async_view, name='generate-pdf-async'),
    path('applications/funding-calculation-async/<int:application_id>/', calculate_funding_async_view, name='funding-calculation-async'),
    path('tasks/<str:task_id>/status/', task_status_view, name='task-status'),
    path('tasks/<str:task_id>/result/', task_result_view, name='task-result'),
]