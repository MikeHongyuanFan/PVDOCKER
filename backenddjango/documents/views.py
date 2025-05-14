from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Document, Note, Fee, Repayment, Ledger, NoteComment
from .serializers import (
    DocumentSerializer,
    NoteSerializer,
    FeeSerializer,
    RepaymentSerializer,
    LedgerSerializer,
    ApplicationLedgerSerializer,
    NoteCommentSerializer
)
from .filters import DocumentFilter, NoteFilter, FeeFilter, RepaymentFilter, NoteCommentFilter
from users.permissions import IsAdmin, IsAdminOrBroker, IsAdminOrBD, IsAdminOrBrokerOrBD, CanAccessNote
from django.http import FileResponse
import os


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing documents
    """
    queryset = Document.objects.all().order_by('-created_at')
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DocumentFilter
    search_fields = ['title', 'description', 'file_name']
    ordering_fields = ['created_at', 'updated_at', 'title']
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrBrokerOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter documents based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see documents associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(
                    application__borrowers=user.borrower_profile
                ) | queryset.filter(
                    borrower=user.borrower_profile
                )
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download a document
        """
        document = self.get_object()
        file_path = document.file.path
        
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=document.file_name)
        else:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)


class DocumentCreateVersionView(GenericAPIView):
    """
    API endpoint for creating a new version of a document
    """
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrBrokerOrBD]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create a new document with the same metadata but new file
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_document = serializer.save(
                title=document.title,
                description=document.description,
                document_type=document.document_type,
                application=document.application,
                borrower=document.borrower,
                created_by=request.user,
                version=document.version + 1,
                previous_version=document
            )
            return Response(self.get_serializer(new_document).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing notes
    """
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NoteFilter
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title', 'remind_date']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrBrokerOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter notes based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see notes associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(
                    application__borrowers=user.borrower_profile
                ) | queryset.filter(
                    borrower=user.borrower_profile
                )
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get all comments for a note
        """
        note = self.get_object()
        comments = note.comments.all()
        serializer = NoteCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """
        Add a comment to a note
        """
        note = self.get_object()
        # Create a copy of the request data to avoid modifying the original
        data = request.data.copy()
        # Add the note ID to the data
        data['note'] = note.id
        serializer = NoteCommentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(note=note, created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing note comments
    """
    queryset = NoteComment.objects.all().order_by('created_at')
    serializer_class = NoteCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NoteCommentFilter
    search_fields = ['content']
    ordering_fields = ['created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrBrokerOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter comments based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(note__application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(note__application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see comments associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(
                    note__application__borrowers=user.borrower_profile
                ) | queryset.filter(
                    note__borrower=user.borrower_profile
                )
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing fees
    """
    queryset = Fee.objects.all().order_by('due_date')
    serializer_class = FeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FeeFilter
    search_fields = ['description']
    ordering_fields = ['due_date', 'paid_date', 'amount', 'fee_type']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter fees based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see fees associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(application__borrowers=user.borrower_profile)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FeeMarkPaidView(GenericAPIView):
    """
    API endpoint for marking a fee as paid
    """
    serializer_class = FeeSerializer
    permission_classes = [IsAdminOrBD]
    
    def post(self, request, pk):
        try:
            fee = Fee.objects.get(pk=pk)
        except Fee.DoesNotExist:
            return Response({'error': 'Fee not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Mark the fee as paid
        fee.paid_date = request.data.get('paid_date', timezone.now().date())
        fee.save()
        
        return Response(self.get_serializer(fee).data)


class RepaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing repayments
    """
    queryset = Repayment.objects.all().order_by('due_date')
    serializer_class = RepaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RepaymentFilter
    ordering_fields = ['due_date', 'paid_date', 'amount']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter repayments based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see repayments associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(application__borrowers=user.borrower_profile)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RepaymentMarkPaidView(GenericAPIView):
    """
    API endpoint for marking a repayment as paid
    """
    serializer_class = RepaymentSerializer
    permission_classes = [IsAdminOrBD]
    
    def post(self, request, pk):
        try:
            repayment = Repayment.objects.get(pk=pk)
        except Repayment.DoesNotExist:
            return Response({'error': 'Repayment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Mark the repayment as paid
        repayment.paid_date = request.data.get('paid_date', timezone.now().date())
        repayment.save()
        
        return Response(self.get_serializer(repayment).data)


class ApplicationLedgerView(GenericAPIView):
    """
    API endpoint for getting the ledger for an application
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationLedgerSerializer
    
    def get(self, request, application_id):
        # Check if the user has access to this application
        user = request.user
        
        if user.role == 'admin':
            pass  # Admin has access to all applications
        elif user.role == 'broker':
            if not Application.objects.filter(id=application_id, broker__user=user).exists():
                return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                if not Application.objects.filter(id=application_id, bd=user.bdm_profile).exists():
                    return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
        elif user.role == 'client':
            if hasattr(user, 'borrower_profile'):
                if not Application.objects.filter(id=application_id, borrowers=user.borrower_profile).exists():
                    return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get the application
        try:
            application = Application.objects.get(pk=application_id)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the ledger entries
        ledger_entries = Ledger.objects.filter(application=application).order_by('-transaction_date')
        
        # Get the fees and repayments
        fees = Fee.objects.filter(application=application).order_by('due_date')
        repayments = Repayment.objects.filter(application=application).order_by('due_date')
        
        # Serialize the data
        serializer = ApplicationLedgerSerializer({
            'application': application,
            'ledger_entries': ledger_entries,
            'fees': fees,
            'repayments': repayments
        })
        
        return Response(serializer.data)
