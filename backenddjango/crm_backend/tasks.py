"""
Core asynchronous tasks for the CRM Loan Management System.
This module contains tasks that are not specific to any particular app.
"""

from celery import shared_task
from celery.result import AsyncResult
from django.conf import settings
import time
import json
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def generic_task(self, task_type, *args, **kwargs):
    """
    Generic task that can be used to run any function asynchronously.
    
    Args:
        task_type: Type of task to run
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Result of the function
    """
    logger.info(f"Running generic task of type {task_type}")
    
    # Update task state to started
    self.update_state(state='STARTED', meta={'progress': 0, 'message': f'Starting {task_type} task'})
    
    try:
        # Determine which function to call based on task_type
        if task_type == 'generate_document':
            from applications.services import generate_document
            result = generate_document(*args, **kwargs)
            return {'document_id': result.id if result else None}
            
        elif task_type == 'generate_pdf':
            from documents.services import generate_document_from_template
            result = generate_document_from_template(*args, **kwargs)
            return {'document_id': result.id if result else None}
            
        elif task_type == 'funding_calculation':
            from applications.services import calculate_funding
            result, history = calculate_funding(*args, **kwargs)
            return {'calculation_result': result, 'history_id': history.id if history else None}
            
        else:
            raise ValueError(f"Unknown task type: {task_type}")
            
    except Exception as e:
        logger.exception(f"Error in generic task of type {task_type}: {str(e)}")
        # Update task state to failure
        self.update_state(state='FAILURE', meta={'message': str(e)})
        raise


@shared_task(bind=True)
def generate_document_async(self, application_id, document_type, user_id):
    """
    Generate a document asynchronously.
    
    Args:
        application_id: ID of the application
        document_type: Type of document to generate
        user_id: ID of the user generating the document
        
    Returns:
        Dictionary with document ID if successful, None otherwise
    """
    from applications.services import generate_document
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    logger.info(f"Generating document of type {document_type} for application {application_id}")
    
    # Update task state to started
    self.update_state(state='STARTED', meta={'progress': 0, 'message': 'Starting document generation'})
    
    try:
        # Get user
        user = User.objects.get(id=user_id)
        
        # Update progress
        self.update_state(state='STARTED', meta={'progress': 25, 'message': 'Preparing document'})
        
        # Generate document
        document = generate_document(application_id, document_type, user)
        
        # Update progress
        self.update_state(state='STARTED', meta={'progress': 75, 'message': 'Finalizing document'})
        
        # Simulate some processing time
        time.sleep(1)
        
        # Return result
        if document:
            return {'document_id': document.id, 'document_url': document.file.url if document.file else None}
        else:
            return {'document_id': None, 'error': 'Failed to generate document'}
            
    except Exception as e:
        logger.exception(f"Error generating document: {str(e)}")
        # Update task state to failure
        self.update_state(state='FAILURE', meta={'message': str(e)})
        raise


@shared_task(bind=True)
def generate_pdf_async(self, template_name, context, output_filename, document_type, application_id, user_id):
    """
    Generate a PDF document asynchronously.
    
    Args:
        template_name: Name of the template file
        context: Context data for the template
        output_filename: Name for the output file
        document_type: Type of document being generated
        application_id: ID of the application
        user_id: ID of the user generating the document
        
    Returns:
        Dictionary with document ID if successful, None otherwise
    """
    from documents.services import generate_document_from_template
    from applications.models import Application
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    logger.info(f"Generating PDF document from template {template_name}")
    
    # Update task state to started
    self.update_state(state='STARTED', meta={'progress': 0, 'message': 'Starting PDF generation'})
    
    try:
        # Get user and application
        user = User.objects.get(id=user_id)
        application = Application.objects.get(id=application_id)
        
        # Update progress
        self.update_state(state='STARTED', meta={'progress': 25, 'message': 'Rendering template'})
        
        # Generate PDF
        document = generate_document_from_template(
            template_name=template_name,
            context=context,
            output_filename=output_filename,
            document_type=document_type,
            application=application,
            user=user
        )
        
        # Update progress
        self.update_state(state='STARTED', meta={'progress': 75, 'message': 'Finalizing PDF'})
        
        # Simulate some processing time
        time.sleep(1)
        
        # Return result
        if document:
            return {'document_id': document.id, 'document_url': document.file.url if document.file else None}
        else:
            return {'document_id': None, 'error': 'Failed to generate PDF'}
            
    except Exception as e:
        logger.exception(f"Error generating PDF: {str(e)}")
        # Update task state to failure
        self.update_state(state='FAILURE', meta={'message': str(e)})
        raise


@shared_task(bind=True)
def calculate_funding_async(self, application_id, calculation_input, user_id):
    """
    Calculate funding asynchronously.
    
    Args:
        application_id: ID of the application
        calculation_input: Dictionary containing calculation input parameters
        user_id: ID of the user performing the calculation
        
    Returns:
        Dictionary with calculation result and history ID
    """
    from applications.services import calculate_funding
    from applications.models import Application
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    logger.info(f"Calculating funding for application {application_id}")
    
    # Update task state to started
    self.update_state(state='STARTED', meta={'progress': 0, 'message': 'Starting funding calculation'})
    
    try:
        # Get user and application
        user = User.objects.get(id=user_id)
        application = Application.objects.get(id=application_id)
        
        # Update progress
        self.update_state(state='STARTED', meta={'progress': 25, 'message': 'Processing calculation inputs'})
        
        # Calculate funding
        calculation_result, funding_history = calculate_funding(
            application=application,
            calculation_input=calculation_input,
            user=user
        )
        
        # Update progress
        self.update_state(state='STARTED', meta={'progress': 75, 'message': 'Finalizing calculation'})
        
        # Simulate some processing time
        time.sleep(1)
        
        # Return result
        return {
            'calculation_result': calculation_result,
            'history_id': funding_history.id if funding_history else None
        }
            
    except Exception as e:
        logger.exception(f"Error calculating funding: {str(e)}")
        # Update task state to failure
        self.update_state(state='FAILURE', meta={'message': str(e)})
        raise


def get_task_status(task_id):
    """
    Get the status of a task.
    
    Args:
        task_id: ID of the task
        
    Returns:
        Dictionary with task status information
    """
    result = AsyncResult(task_id)
    
    response = {
        'task_id': task_id,
        'status': result.state,
        'progress': 0,
        'message': '',
    }
    
    if result.state == 'PENDING':
        response['message'] = 'Task is pending'
    elif result.state == 'STARTED':
        if result.info and isinstance(result.info, dict):
            response['progress'] = result.info.get('progress', 0)
            response['message'] = result.info.get('message', 'Task is in progress')
    elif result.state == 'SUCCESS':
        response['progress'] = 100
        response['message'] = 'Task completed successfully'
    elif result.state == 'FAILURE':
        response['message'] = str(result.info) if result.info else 'Task failed'
    
    return response


def get_task_result(task_id):
    """
    Get the result of a completed task.
    
    Args:
        task_id: ID of the task
        
    Returns:
        Dictionary with task result information
    """
    result = AsyncResult(task_id)
    
    if result.state == 'SUCCESS':
        return {
            'task_id': task_id,
            'status': 'SUCCESS',
            'result': result.get(),
        }
    elif result.state == 'FAILURE':
        return {
            'task_id': task_id,
            'status': 'FAILURE',
            'error': str(result.info) if result.info else 'Unknown error',
        }
    else:
        return {
            'task_id': task_id,
            'status': result.state,
            'message': 'Task is not yet complete',
        }