from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowerAssetViewSet, GuarantorAssetViewSet, GuarantorViewSet, BorrowerViewSet

router = DefaultRouter()
router.register(r'guarantors', GuarantorViewSet)
router.register(r'borrowers', BorrowerViewSet)

urlpatterns = [
    path('borrowers/<int:borrower_id>/assets/', BorrowerAssetViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='borrower-assets'),
    path('borrowers/<int:borrower_id>/assets/<int:pk>/', BorrowerAssetViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='borrower-asset-detail'),
    
    path('guarantors/<int:guarantor_id>/assets/', GuarantorAssetViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='guarantor-assets'),
    path('guarantors/<int:guarantor_id>/assets/<int:pk>/', GuarantorAssetViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='guarantor-asset-detail'),
    
    path('', include(router.urls)),
]
