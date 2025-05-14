"""
DRF-Spectacular Settings Configuration
Add these settings to your Django settings.py file
"""

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    'rest_framework',
    'drf_spectacular',
    # ... other apps
]

# Configure REST_FRAMEWORK settings
REST_FRAMEWORK = {
    # ... existing settings
    
    # Set drf-spectacular as the default schema generator
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# DRF-Spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'CRM Loan Management System API',
    'DESCRIPTION': 'A comprehensive CRM system for loan applications with fully synchronized frontend and backend development.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
    # UI customization
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    
    # JWT token configuration
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
    
    # Schema customization
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_NO_READ_ONLY_REQUIRED': False,
    
    # Preprocessing hooks
    'PREPROCESSING_HOOKS': [
        'drf_spectacular.hooks.preprocess_exclude_path_format',
    ],
    
    # Postprocessing hooks
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums',
    ],
    
    # Tags configuration for API grouping
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
