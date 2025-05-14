#!/bin/bash

# DRF-Spectacular Setup Script
# This script will set up drf-spectacular for your Django REST Framework project

echo "Setting up drf-spectacular for OpenAPI 3.0 documentation..."

# Install drf-spectacular
echo "Installing drf-spectacular..."
pip install drf-spectacular

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "Failed to install drf-spectacular. Please check your Python environment."
    exit 1
fi

echo "drf-spectacular installed successfully!"

# Create a backup of settings.py
echo "Creating backup of settings.py..."
if [ -f "backenddjango/crm_backend/settings.py" ]; then
    cp backenddjango/crm_backend/settings.py backenddjango/crm_backend/settings.py.bak
    echo "Backup created at backenddjango/crm_backend/settings.py.bak"
else
    echo "Warning: Could not find settings.py at the expected location."
    echo "Please manually update your settings.py file using the provided drf_spectacular_settings.py file."
fi

# Create a backup of urls.py
echo "Creating backup of urls.py..."
if [ -f "backenddjango/crm_backend/urls.py" ]; then
    cp backenddjango/crm_backend/urls.py backenddjango/crm_backend/urls.py.bak
    echo "Backup created at backenddjango/crm_backend/urls.py.bak"
else
    echo "Warning: Could not find urls.py at the expected location."
    echo "Please manually update your urls.py file using the provided drf_spectacular_urls.py file."
fi

echo ""
echo "Setup complete! Please follow these next steps:"
echo ""
echo "1. Add drf_spectacular to INSTALLED_APPS in your settings.py:"
echo "   INSTALLED_APPS = ["
echo "       # ... existing apps"
echo "       'rest_framework',"
echo "       'drf_spectacular',"
echo "       # ... other apps"
echo "   ]"
echo ""
echo "2. Configure REST_FRAMEWORK in your settings.py:"
echo "   REST_FRAMEWORK = {"
echo "       # ... existing settings"
echo "       'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',"
echo "   }"
echo ""
echo "3. Add SPECTACULAR_SETTINGS to your settings.py (see drf_spectacular_settings.py for details)"
echo ""
echo "4. Add the following URL patterns to your urls.py:"
echo "   from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView"
echo ""
echo "   urlpatterns = ["
echo "       # ... existing patterns"
echo "       path('api/schema/', SpectacularAPIView.as_view(), name='schema'),"
echo "       path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),"
echo "       path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),"
echo "       # ... other patterns"
echo "   ]"
echo ""
echo "5. Generate your schema file with:"
echo "   python manage.py spectacular --file schema.yaml"
echo ""
echo "6. For JSON format:"
echo "   python manage.py spectacular --file schema.json --format openapi-json"
echo ""
echo "7. For Postman collection export:"
echo "   python manage.py spectacular --file postman_collection.json --format openapi-json"
echo "   Then import the JSON file into Postman"
echo ""
echo "See the provided example files for advanced configuration options:"
echo "- drf_spectacular_setup.py: Complete setup instructions"
echo "- drf_spectacular_settings.py: Settings configuration"
echo "- drf_spectacular_urls.py: URL configuration"
echo "- drf_spectacular_examples.py: Usage examples for ViewSets, serializers, etc."
echo ""
echo "Documentation is now available at:"
echo "- Swagger UI: http://localhost:8000/api/swagger/"
echo "- ReDoc: http://localhost:8000/api/redoc/"
echo "- Schema: http://localhost:8000/api/schema/"
