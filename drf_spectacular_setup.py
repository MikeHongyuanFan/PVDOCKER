"""
DRF-Spectacular Setup Script for Django REST Framework
This script provides instructions for setting up drf-spectacular to generate
OpenAPI 3.0 documentation for your Django REST Framework project.
"""

# Step 1: Install drf-spectacular
# pip install drf-spectacular

# Step 2: Add drf-spectacular to INSTALLED_APPS in settings.py
"""
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'drf_spectacular',
    # ... other apps
]
"""

# Step 3: Configure REST_FRAMEWORK settings in settings.py
"""
REST_FRAMEWORK = {
    # ... other settings
    
    # Set drf-spectacular as the default schema generator
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
"""

# Step 4: Add drf-spectacular settings in settings.py
"""
SPECTACULAR_SETTINGS = {
    'TITLE': 'CRM Loan Management System API',
    'DESCRIPTION': 'A comprehensive CRM system for loan applications with fully synchronized frontend and backend development.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,  # Exclude the schema view from the schema itself
    
    # Optional UI customization
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    
    # JWT token configuration
    'SECURITY': [
        {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'Enter your JWT token in the format: Bearer <token>'
            }
        }
    ],
    
    # Schema customization
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_NO_READ_ONLY_REQUIRED': False,
    
    # Preprocessing hooks for ViewSets, Views, etc.
    'PREPROCESSING_HOOKS': [
        'drf_spectacular.hooks.preprocess_exclude_path_format',
    ],
    
    # Postprocessing hooks for the schema
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums',
    ],
    
    # Schema operation customization
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },
    
    # Tags configuration
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',
    'SCHEMA_PATH_PREFIX': r'/api/',
    'TAGS': [
        {'name': 'authentication', 'description': 'Authentication operations'},
        {'name': 'applications', 'description': 'Loan application operations'},
        {'name': 'borrowers', 'description': 'Borrower management operations'},
        {'name': 'brokers', 'description': 'Broker management operations'},
        {'name': 'documents', 'description': 'Document management operations'},
        {'name': 'products', 'description': 'Product management operations'},
        {'name': 'users', 'description': 'User management operations'},
    ],
}
"""

# Step 5: Add drf-spectacular URLs to urls.py
"""
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # ... other URL patterns
    
    # Schema generation endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # ReDoc UI
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # ... other URL patterns
]
"""

# Step 6: Generate schema file (optional)
"""
# Run this command to generate a schema file
python manage.py spectacular --file schema.yaml

# Or for JSON format
python manage.py spectacular --file schema.json --format openapi-json
"""

# Step 7: Advanced Configuration for ViewSets and Custom Actions

# Example: Custom schema for a ViewSet
"""
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample

@extend_schema_view(
    list=extend_schema(
        summary="List all applications",
        description="Returns a list of all loan applications with pagination",
        parameters=[
            OpenApiParameter(name='status', description='Filter by application status', required=False, type=str),
            OpenApiParameter(name='created_after', description='Filter by creation date', required=False, type=str),
        ],
        responses={200: ApplicationListSerializer}
    ),
    retrieve=extend_schema(
        summary="Retrieve an application",
        description="Returns details of a specific loan application",
        responses={200: ApplicationDetailSerializer}
    ),
    create=extend_schema(
        summary="Create a new application",
        description="Create a new loan application",
        request=ApplicationCreateSerializer,
        responses={201: ApplicationDetailSerializer}
    ),
    update=extend_schema(
        summary="Update an application",
        description="Update an existing loan application",
        request=ApplicationUpdateSerializer,
        responses={200: ApplicationDetailSerializer}
    ),
)
class ApplicationViewSet(viewsets.ModelViewSet):
    # Your ViewSet code here
    pass
"""

# Example: Custom schema for a custom action
"""
@extend_schema(
    methods=['post'],
    summary="Submit application for approval",
    description="Submit a loan application for approval process",
    request=ApplicationSubmitSerializer,
    responses={
        200: ApplicationDetailSerializer,
        400: OpenApiResponse(description="Invalid submission data"),
        403: OpenApiResponse(description="Permission denied"),
    },
    examples=[
        OpenApiExample(
            'Successful Submission',
            value={
                'status': 'submitted',
                'submission_date': '2023-05-01T12:00:00Z',
            },
            request_only=True,
        ),
    ],
)
@action(detail=True, methods=['post'])
def submit(self, request, pk=None):
    # Your action code here
    pass
"""

# Step 8: Handling Nested ViewSets
"""
# For nested ViewSets, you can use drf-nested-routers with drf-spectacular
# pip install drf-nested-routers

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'applications', ApplicationViewSet)

# Create a nested router for documents under applications
application_router = routers.NestedDefaultRouter(router, r'applications', lookup='application')
application_router.register(r'documents', DocumentViewSet, basename='application-documents')

urlpatterns = [
    # ... other URL patterns
    path('api/', include(router.urls)),
    path('api/', include(application_router.urls)),
    # ... other URL patterns
]
"""

# Step 9: Custom Serializer Schema
"""
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid example',
            value={
                'id': 123,
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '+1234567890',
                'address': '123 Main St',
            },
            summary='Sample borrower data',
        ),
    ],
    component_name='BorrowerDetail'  # Custom component name
)
class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ['id', 'name', 'email', 'phone', 'address']
"""

# Step 10: Authentication Schema
"""
# For JWT authentication, ensure your settings include:

SPECTACULAR_SETTINGS = {
    # ... other settings
    
    # JWT Authentication
    'SECURITY': [{'Bearer': []}],
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },
}

# Then in your views or viewsets, you can specify which endpoints require authentication:

@extend_schema(
    summary="Create a new application",
    security=[{'Bearer': []}]  # This endpoint requires JWT authentication
)
def create_application(request):
    # Your view code here
    pass
"""

# Step 11: Pagination and Filter Schema
"""
# For custom pagination, you can extend the schema:

from drf_spectacular.utils import extend_schema_field
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_page_size(self, request):
        return super().get_page_size(request)

# For filters:
from django_filters import rest_framework as filters

class ApplicationFilter(filters.FilterSet):
    status = filters.CharFilter(help_text="Filter by application status")
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte', 
                                      help_text="Filter by creation date (format: YYYY-MM-DD)")
    
    class Meta:
        model = Application
        fields = ['status', 'created_after']
"""

print("DRF-Spectacular setup instructions have been created.")
print("Follow the steps in the drf_spectacular_setup.py file to configure your project.")
