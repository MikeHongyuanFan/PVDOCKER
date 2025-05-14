"""
Authentication utilities for integration tests.
"""

from typing import Dict, Tuple, Optional
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


def create_admin_user(
    username: str = "admin_test",
    email: str = "admin_test@example.com",
    password: str = "adminpassword",
    first_name: str = "Admin",
    last_name: str = "Test"
) -> User:
    """
    Create an admin user.
    
    Args:
        username: Username for the admin user
        email: Email for the admin user
        password: Password for the admin user
        first_name: First name for the admin user
        last_name: Last name for the admin user
        
    Returns:
        User: The created admin user
    """
    return User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role='admin'
    )


def get_tokens_for_user(user: User) -> Tuple[str, str]:
    """
    Get access and refresh tokens for a user.
    
    Args:
        user: The user to get tokens for
        
    Returns:
        Tuple[str, str]: Access token and refresh token
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def authenticate_client(client: APIClient, user: User) -> str:
    """
    Authenticate an API client as a user.
    
    Args:
        client: The API client to authenticate
        user: The user to authenticate as
        
    Returns:
        str: The access token
    """
    access_token, _ = get_tokens_for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return access_token


def get_auth_headers(user: User) -> Dict[str, str]:
    """
    Get authentication headers for a user.
    
    Args:
        user: The user to get headers for
        
    Returns:
        Dict[str, str]: Authentication headers
    """
    access_token, _ = get_tokens_for_user(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}


def clear_authentication(client: APIClient) -> None:
    """
    Clear authentication credentials from an API client.
    
    Args:
        client: The API client to clear credentials from
    """
    client.credentials()


def verify_token_valid(client: APIClient, token: str) -> bool:
    """
    Verify that a token is valid by making a request to a protected endpoint.
    
    Args:
        client: The API client to use
        token: The token to verify
        
    Returns:
        bool: True if the token is valid
    """
    # Save current credentials
    current_auth = client.handler._credentials.get('HTTP_AUTHORIZATION', None)
    
    try:
        # Set the token to verify
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Make a request to a protected endpoint
        response = client.get('/api/users/me/')
        
        # Check if the request was successful
        return response.status_code == 200
    finally:
        # Restore original credentials
        if current_auth:
            client.credentials(HTTP_AUTHORIZATION=current_auth)
        else:
            client.credentials()
