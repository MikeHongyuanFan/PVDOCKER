from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.application_views import ApplicationViewSet
from .views.pdf_generation import GenerateFilledFormView

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Enhanced application list endpoint
    path('enhanced-applications/', ApplicationViewSet.as_view({'get': 'enhanced_list'}), name='enhanced-application-list'),
    
    # Application creation with cascade
    path('create-with-cascade/', ApplicationViewSet.as_view({'post': 'create'}), name='application-list-create'),
    
    # Application validation
    path('validate-schema/', ApplicationViewSet.as_view({'post': 'validate_schema'}), name='validate-application-schema'),
    
    # Application signature
    path('<int:pk>/signature/', ApplicationViewSet.as_view({'post': 'signature'}), name='application-signature'),
    
    # Application stage update
    path('<int:pk>/stage/', ApplicationViewSet.as_view({'put': 'update_stage'}), name='application-stage-update'),
    
    # Application borrowers update
    path('<int:pk>/borrowers/', ApplicationViewSet.as_view({'put': 'borrowers'}), name='application-borrowers-update'),
    
    # Application sign
    path('<int:pk>/sign/', ApplicationViewSet.as_view({'post': 'sign'}), name='application-sign'),
    
    # Application loan extension
    path('<int:pk>/extend-loan/', ApplicationViewSet.as_view({'post': 'extend_loan'}), name='application-extend-loan'),
    
    # Funding calculation
    path('<int:pk>/funding-calculation/', ApplicationViewSet.as_view({'post': 'funding_calculation'}), name='application-funding-calculation'),
    
    # Funding calculation history
    path('<int:pk>/funding-calculation-history/', ApplicationViewSet.as_view({'get': 'funding_calculation_history'}), name='application-funding-calculation-history'),
    
    # Generate filled PDF form
    path('<int:application_id>/generate-pdf/', GenerateFilledFormView.as_view(), name='application-generate-pdf'),
]
