"""
Response utilities for integration tests.
"""

from typing import Dict, Any, List, Optional, Union
from rest_framework.response import Response
from rest_framework import status


def get_response_data(response: Response) -> Union[Dict[str, Any], List[Any]]:
    """
    Get data from a response, handling both JSON and non-JSON responses.
    
    Args:
        response: The API response
        
    Returns:
        Union[Dict, List]: The response data
    """
    if hasattr(response, 'json'):
        try:
            return response.json()
        except ValueError:
            return {}
    return response.data


def get_paginated_results(response: Response) -> List[Dict[str, Any]]:
    """
    Get results from a paginated response.
    
    Args:
        response: The API response
        
    Returns:
        List[Dict]: The results from the paginated response
    """
    data = get_response_data(response)
    
    if isinstance(data, dict) and 'results' in data:
        return data['results']
    
    if isinstance(data, list):
        return data
    
    return []


def get_object_from_response(response: Response, field: str, value: Any) -> Optional[Dict[str, Any]]:
    """
    Get an object from a response by matching a field value.
    
    Args:
        response: The API response
        field: The field to match
        value: The value to match
        
    Returns:
        Optional[Dict]: The matching object, or None if not found
    """
    objects = get_paginated_results(response)
    
    for obj in objects:
        if field in obj and obj[field] == value:
            return obj
    
    return None


def get_error_detail(response: Response, field: Optional[str] = None) -> Union[str, Dict[str, List[str]], None]:
    """
    Get error details from a response.
    
    Args:
        response: The API response
        field: Optional field to get errors for
        
    Returns:
        Union[str, Dict, None]: The error details
    """
    if response.status_code < 400:
        return None
    
    data = get_response_data(response)
    
    if not data:
        return None
    
    if 'detail' in data:
        return data['detail']
    
    if field and field in data:
        return data[field]
    
    return data


def is_success_response(response: Response) -> bool:
    """
    Check if a response indicates success.
    
    Args:
        response: The API response
        
    Returns:
        bool: True if the response indicates success
    """
    return 200 <= response.status_code < 300


def is_error_response(response: Response) -> bool:
    """
    Check if a response indicates an error.
    
    Args:
        response: The API response
        
    Returns:
        bool: True if the response indicates an error
    """
    return response.status_code >= 400


def is_validation_error(response: Response) -> bool:
    """
    Check if a response indicates a validation error.
    
    Args:
        response: The API response
        
    Returns:
        bool: True if the response indicates a validation error
    """
    return response.status_code == status.HTTP_400_BAD_REQUEST


def is_permission_denied(response: Response) -> bool:
    """
    Check if a response indicates permission denied.
    
    Args:
        response: The API response
        
    Returns:
        bool: True if the response indicates permission denied
    """
    return response.status_code == status.HTTP_403_FORBIDDEN


def is_not_found(response: Response) -> bool:
    """
    Check if a response indicates not found.
    
    Args:
        response: The API response
        
    Returns:
        bool: True if the response indicates not found
    """
    return response.status_code == status.HTTP_404_NOT_FOUND
