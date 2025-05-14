"""
DRF-Spectacular URL Configuration
Add these URL patterns to your project's urls.py file
"""

from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Add these URL patterns to your urlpatterns list
urlpatterns = [
    # ... your existing URL patterns
    
    # Schema generation endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # ReDoc UI
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # ... your other URL patterns
]
