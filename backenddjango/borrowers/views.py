from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Borrower, Guarantor, Asset, Liability
from applications.serializers_asset import CompanyAssetSerializer, GuarantorAssetSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import GuarantorSerializer, BorrowerListSerializer, BorrowerDetailSerializer

class BorrowerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing borrowers
    """
    queryset = Borrower.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BorrowerListSerializer
        return BorrowerDetailSerializer

class BorrowerAssetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing company borrower assets
    """
    serializer_class = CompanyAssetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Get assets for a specific borrower
        """
        borrower_id = self.kwargs.get('borrower_id')
        return Asset.objects.filter(borrower_id=borrower_id)
    
    def perform_create(self, serializer):
        """
        Create a new asset for a borrower
        """
        borrower_id = self.kwargs.get('borrower_id')
        borrower = Borrower.objects.get(id=borrower_id)
        serializer.save(borrower=borrower, created_by=self.request.user)


class GuarantorAssetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing guarantor assets
    """
    serializer_class = GuarantorAssetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Get assets for a specific guarantor
        """
        guarantor_id = self.kwargs.get('guarantor_id')
        return Asset.objects.filter(guarantor_id=guarantor_id)
    
    def perform_create(self, serializer):
        """
        Create a new asset for a guarantor
        """
        guarantor_id = self.kwargs.get('guarantor_id')
        guarantor = Guarantor.objects.get(id=guarantor_id)
        serializer.save(guarantor=guarantor, created_by=self.request.user)


class GuarantorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing guarantors
    """
    queryset = Guarantor.objects.all()
    serializer_class = GuarantorSerializer
    permission_classes = [IsAuthenticated]
