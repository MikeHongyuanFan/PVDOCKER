"""
Request utilities for integration tests.
"""

from typing import Dict, Any, Optional, Union
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.response import Response


def build_url(url_name: str, pk: Optional[int] = None, query_params: Optional[Dict[str, Any]] = None) -> str:
    """
    Build a URL for an API request.
    
    Args:
        url_name: The name of the URL to reverse
        pk: Optional primary key for detail views
        query_params: Optional query parameters
        
    Returns:
        str: The URL
    """
    url = reverse(url_name, args=[pk] if pk else None)
    
    if query_params:
        query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
        url = f"{url}?{query_string}"
    
    return url


def make_api_request(
    client: APIClient,
    method: str,
    url_name: str,
    data: Optional[Dict[str, Any]] = None,
    pk: Optional[int] = None,
    query_params: Optional[Dict[str, Any]] = None,
    format: str = 'json',
    files: Optional[Dict[str, Any]] = None
) -> Response:
    """
    Make an API request.
    
    Args:
        client: The API client
        method: HTTP method (GET, POST, PUT, PATCH, DELETE)
        url_name: The name of the URL to reverse
        data: Optional data to send
        pk: Optional primary key for detail views
        query_params: Optional query parameters
        format: Request format (default: json)
        files: Optional files to upload
        
    Returns:
        Response: The API response
    """
    url = build_url(url_name, pk, query_params)
    
    if method.upper() == 'GET':
        return client.get(url, format=format)
    elif method.upper() == 'POST':
        if files:
            return client.post(url, data=data, files=files)
        return client.post(url, data=data, format=format)
    elif method.upper() == 'PUT':
        if files:
            return client.put(url, data=data, files=files)
        return client.put(url, data=data, format=format)
    elif method.upper() == 'PATCH':
        if files:
            return client.patch(url, data=data, files=files)
        return client.patch(url, data=data, format=format)
    elif method.upper() == 'DELETE':
        return client.delete(url)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")


def paginated_get_all(client: APIClient, url_name: str, query_params: Optional[Dict[str, Any]] = None) -> list:
    """
    Get all objects from a paginated API endpoint.
    
    Args:
        client: The API client
        url_name: The name of the URL to reverse
        query_params: Optional query parameters
        
    Returns:
        list: All objects from all pages
    """
    url = build_url(url_name, query_params=query_params)
    response = client.get(url)
    
    if response.status_code != 200:
        raise ValueError(f"Failed to get objects: {response.content}")
    
    data = response.json()
    
    # If not paginated, return the data directly
    if not isinstance(data, dict) or 'results' not in data:
        return data
    
    results = data['results']
    
    # If there are more pages, fetch them
    while data.get('next'):
        response = client.get(data['next'])
        if response.status_code != 200:
            raise ValueError(f"Failed to get objects: {response.content}")
        
        data = response.json()
        results.extend(data['results'])
    
    return results
