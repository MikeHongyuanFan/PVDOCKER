"""
DRF-Spectacular Usage Examples
This file contains examples for customizing your API schema documentation
"""

# Example 1: Custom schema for a ViewSet
"""
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

@extend_schema_view(
    list=extend_schema(
        summary="List all loan applications",
        description="Returns a paginated list of all loan applications",
        parameters=[
            OpenApiParameter(name='status', description='Filter by application status', required=False, type=str),
            OpenApiParameter(name='created_after', description='Filter by creation date (YYYY-MM-DD)', required=False, type=str),
        ],
    ),
    retrieve=extend_schema(
        summary="Retrieve a loan application",
        description="Returns details of a specific loan application",
    ),
    create=extend_schema(
        summary="Create a new loan application",
        description="Create a new loan application with initial data",
    ),
    update=extend_schema(
        summary="Update a loan application",
        description="Update an existing loan application",
    ),
    partial_update=extend_schema(
        summary="Partially update a loan application",
        description="Update specific fields of an existing loan application",
    ),
    destroy=extend_schema(
        summary="Delete a loan application",
        description="Delete an existing loan application",
    ),
)
class ApplicationViewSet(viewsets.ModelViewSet):
    # Your ViewSet code here
    pass
"""

# Example 2: Custom schema for a custom action
"""
from drf_spectacular.utils import extend_schema, OpenApiResponse

class ApplicationViewSet(viewsets.ModelViewSet):
    # ... your ViewSet code
    
    @extend_schema(
        summary="Submit application for approval",
        description="Submit a loan application for approval process",
        request=ApplicationSubmitSerializer,
        responses={
            200: ApplicationDetailSerializer,
            400: OpenApiResponse(description="Invalid submission data"),
            403: OpenApiResponse(description="Permission denied"),
        },
    )
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        # Your action code here
        pass
"""

# Example 3: Custom serializer schema
"""
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid borrower data',
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
)
class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ['id', 'name', 'email', 'phone', 'address']
"""

# Example 4: Custom field schema
"""
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

class ApplicationSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_status_display(self, obj):
        return obj.get_status_display()
    
    class Meta:
        model = Application
        fields = ['id', 'status', 'status_display']
"""

# Example 5: Nested ViewSets with drf-nested-routers
"""
# In urls.py
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

# Example 6: Authentication and permissions
"""
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Create a new application",
    description="Create a new loan application (requires authentication)",
    security=[{'Bearer': []}]  # This endpoint requires JWT authentication
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_application(request):
    # Your view code here
    pass
"""

# Example 7: Pagination and filtering
"""
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, OpenApiParameter

class ApplicationFilter(filters.FilterSet):
    status = filters.CharFilter(help_text="Filter by application status")
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte', 
                                      help_text="Filter by creation date (format: YYYY-MM-DD)")
    
    class Meta:
        model = Application
        fields = ['status', 'created_after']

@extend_schema(
    parameters=[
        OpenApiParameter(name='page', description='Page number', required=False, type=int),
        OpenApiParameter(name='page_size', description='Number of results per page', required=False, type=int),
    ],
)
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filterset_class = ApplicationFilter
    pagination_class = PageNumberPagination
"""

# Example 8: Generating schema files
"""
# Run these commands to generate schema files

# Generate YAML schema
python manage.py spectacular --file schema.yaml

# Generate JSON schema
python manage.py spectacular --file schema.json --format openapi-json

# Generate schema with specific urlconf
python manage.py spectacular --urlconf=myproject.urls --file schema.yaml

# Generate schema for specific patterns
python manage.py spectacular --pattern=api/v1 --file schema_v1.yaml
"""
