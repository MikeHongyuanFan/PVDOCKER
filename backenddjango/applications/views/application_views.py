from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from ..models import Application

class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Application instances.
    """
    queryset = Application.objects.all()
    
    def get_queryset(self):
        """
        Get the queryset with optimized prefetching for list and detail views
        """
        queryset = Application.objects.all()
        
        if self.action == 'list':
            # Optimize the list view with prefetches for the enhanced fields
            queryset = queryset.select_related('bd').prefetch_related(
                'borrowers',
                'guarantors',
                'securityproperty_set'
            )
        
        return queryset
    
    def get_serializer_class(self):
        from ..serializers import (
            ApplicationCreateSerializer,
            ApplicationDetailSerializer,
            ApplicationListSerializer
        )
        
        if self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action == 'retrieve':
            return ApplicationDetailSerializer
        return ApplicationListSerializer

    @action(detail=True, methods=['post'])
    def signature(self, request, pk=None):
        # Placeholder for signature functionality
        application = self.get_object()
        
        from ..serializers import ApplicationSignatureSerializer
        serializer = ApplicationSignatureSerializer(data=request.data)
        
        if serializer.is_valid():
            # Update application with signature data
            application.signed_by = serializer.validated_data.get('name')
            application.signature_date = serializer.validated_data.get('signature_date')
            application.save()
            
            return Response({"message": "Signature added successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_stage(self, request, pk=None):
        application = self.get_object()
        
        from ..serializers import ApplicationStageUpdateSerializer
        serializer = ApplicationStageUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            application.stage = serializer.validated_data['stage']
            application.save()
            
            # Add note if provided
            if 'notes' in serializer.validated_data and serializer.validated_data['notes']:
                from documents.models import Note
                Note.objects.create(
                    application=application,
                    content=f"Stage updated to {application.get_stage_display()}: {serializer.validated_data['notes']}",
                    created_by=request.user
                )
            
            return Response({"message": "Stage updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def borrowers(self, request, pk=None):
        application = self.get_object()
        
        from ..serializers import ApplicationBorrowerSerializer
        serializer = ApplicationBorrowerSerializer(data=request.data)
        
        if serializer.is_valid():
            from borrowers.models import Borrower
            
            # Clear existing borrowers
            application.borrowers.clear()
            
            # Add new borrowers
            borrower_ids = serializer.validated_data['borrower_ids']
            borrowers = Borrower.objects.filter(id__in=borrower_ids)
            
            if len(borrowers) != len(borrower_ids):
                return Response({"error": "One or more borrower IDs are invalid"}, status=status.HTTP_400_BAD_REQUEST)
            
            application.borrowers.add(*borrowers)
            
            return Response({"message": "Borrowers updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def sign(self, request, pk=None):
        application = self.get_object()
        
        # Check if application is already signed
        if application.signed_by:
            return Response({"error": "Application is already signed"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update application with signature data
        application.signed_by = request.data.get('name', '')
        application.signature_date = request.data.get('date')
        application.save()
        
        return Response({"message": "Application signed successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def extend_loan(self, request, pk=None):
        application = self.get_object()
        
        from ..serializers import LoanExtensionSerializer
        serializer = LoanExtensionSerializer(data=request.data)
        
        if serializer.is_valid():
            # Update application with new loan terms
            application.interest_rate = serializer.validated_data['new_rate']
            application.loan_amount = serializer.validated_data['new_loan_amount']
            application.save()
            
            # Create a note about the loan extension
            from documents.models import Note
            Note.objects.create(
                application=application,
                content=f"Loan extended with new terms: Rate {serializer.validated_data['new_rate']}%, Amount ${serializer.validated_data['new_loan_amount']}, Repayment ${serializer.validated_data['new_repayment']}",
                created_by=request.user
            )
            
            return Response({"message": "Loan extended successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def funding_calculation(self, request, pk=None):
        application = self.get_object()
        
        from ..serializers import FundingCalculationInputSerializer
        serializer = FundingCalculationInputSerializer(data=request.data)
        
        if serializer.is_valid():
            from ..services import calculate_funding
            
            try:
                calculation_result, funding_history = calculate_funding(
                    application=application,
                    calculation_input=serializer.validated_data,
                    user=request.user
                )
                
                return Response({
                    "message": "Funding calculation completed successfully",
                    "result": calculation_result,
                    "history_id": funding_history.id
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def funding_calculation_history(self, request, pk=None):
        application = self.get_object()
        
        from ..models import FundingCalculationHistory
        history = FundingCalculationHistory.objects.filter(application=application).order_by('-created_at')
        
        from ..serializers import FundingCalculationHistorySerializer
        serializer = FundingCalculationHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def enhanced_list(self, request):
        """
        Enhanced list view with additional fields for the application dashboard
        """
        queryset = self.get_queryset()
        
        # Apply filters if provided
        from ..filters import ApplicationFilter
        filtered_queryset = ApplicationFilter(request.GET, queryset=queryset).qs
        
        # Apply pagination
        page_size = request.query_params.get('page_size', 10)
        paginator = self.paginator
        if paginator is not None:
            paginator.page_size = page_size
            
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            from ..serializers import ApplicationListSerializer
            serializer = ApplicationListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ApplicationListSerializer(filtered_queryset, many=True, context={'request': request})
        return Response(serializer.data)
    @action(detail=False, methods=['post'])
    def validate_schema(self, request):
        # This is a placeholder for schema validation
        # In a real implementation, you would validate the request data against a schema
        return Response({"valid": True}, status=status.HTTP_200_OK)
