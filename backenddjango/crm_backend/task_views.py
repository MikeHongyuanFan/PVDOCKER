"""
Views for handling asynchronous tasks in the CRM Loan Management System.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from .tasks import (
    generate_document_async,
    generate_pdf_async,
    calculate_funding_async,
    get_task_status,
    get_task_result
)
from applications.models import Application


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_document_async_view(request, application_id):
    """
    Generate a document asynchronously.
    """
    try:
        # Check if application exists
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return Response(
            {'error': f'Application with ID {application_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get document type from request
    document_type = request.data.get('document_type')
    if not document_type:
        return Response(
            {'error': 'document_type is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Start asynchronous task
    task = generate_document_async.delay(
        application_id=application_id,
        document_type=document_type,
        user_id=request.user.id
    )
    
    # Return task information
    return Response({
        'task_id': task.id,
        'status': task.status,
        'status_url': request.build_absolute_uri(reverse('task-status', kwargs={'task_id': task.id})),
        'result_url': request.build_absolute_uri(reverse('task-result', kwargs={'task_id': task.id}))
    }, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_pdf_async_view(request, application_id):
    """
    Generate a PDF document asynchronously.
    """
    try:
        # Check if application exists
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return Response(
            {'error': f'Application with ID {application_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get required parameters from request
    template_name = request.data.get('template_name')
    output_filename = request.data.get('output_filename')
    document_type = request.data.get('document_type')
    context = request.data.get('context', {})
    
    # Validate required parameters
    if not template_name or not output_filename or not document_type:
        return Response(
            {'error': 'template_name, output_filename, and document_type are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Start asynchronous task
    task = generate_pdf_async.delay(
        template_name=template_name,
        context=context,
        output_filename=output_filename,
        document_type=document_type,
        application_id=application_id,
        user_id=request.user.id
    )
    
    # Return task information
    return Response({
        'task_id': task.id,
        'status': task.status,
        'status_url': request.build_absolute_uri(reverse('task-status', kwargs={'task_id': task.id})),
        'result_url': request.build_absolute_uri(reverse('task-result', kwargs={'task_id': task.id}))
    }, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_funding_async_view(request, application_id):
    """
    Calculate funding asynchronously.
    """
    try:
        # Check if application exists
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return Response(
            {'error': f'Application with ID {application_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get calculation input from request
    calculation_input = request.data
    
    # Start asynchronous task
    task = calculate_funding_async.delay(
        application_id=application_id,
        calculation_input=calculation_input,
        user_id=request.user.id
    )
    
    # Return task information
    return Response({
        'task_id': task.id,
        'status': task.status,
        'status_url': request.build_absolute_uri(reverse('task-status', kwargs={'task_id': task.id})),
        'result_url': request.build_absolute_uri(reverse('task-result', kwargs={'task_id': task.id}))
    }, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_status_view(request, task_id):
    """
    Get the status of a task.
    """
    status_info = get_task_status(task_id)
    return Response(status_info)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_result_view(request, task_id):
    """
    Get the result of a completed task.
    """
    result_info = get_task_result(task_id)
    
    if result_info['status'] not in ['SUCCESS', 'FAILURE']:
        return Response(
            {'error': 'Task is not yet complete', 'status': result_info['status']},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response(result_info)