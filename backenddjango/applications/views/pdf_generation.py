import os
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404, FileResponse
from ..models import Application
from ..utils.pdf_filler import fill_pdf_form
from users.permissions import IsAdminOrBroker
from ..serializers import GeneratePDFSerializer 
from rest_framework import generics, status

logger = logging.getLogger(__name__)

class GenerateFilledFormView(generics.GenericAPIView):
    """
    API endpoint for generating a filled PDF form from an Application instance.
    """
    permission_classes = [IsAuthenticated, IsAdminOrBroker]
    serializer_class = GeneratePDFSerializer
    
    def get(self, request, application_id):
        """
        Generate a filled PDF form from an Application instance.
        
        Args:
            request: The HTTP request
            application_id: The ID of the Application to generate a PDF for
            
        Returns:
            Response with the path to the generated PDF and a list of missing fields
        """
        try:
            # Get the application
            try:
                application = Application.objects.get(id=application_id)
            except Application.DoesNotExist:
                return Response(
                    {"error": f"Application with ID {application_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if user has permission to access this application
            if not self.has_application_permission(request.user, application):
                return Response(
                    {"error": "You don't have permission to access this application"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Get optional parameters
            template_name = request.query_params.get('template_name', 'default_template')
            output_format = request.query_params.get('output_format', 'pdf')
            
            # Create the output directory if it doesn't exist
            output_dir = os.path.join(settings.MEDIA_ROOT, 'application_forms')
            os.makedirs(output_dir, exist_ok=True)
            
            # Define the output path
            output_filename = f"{application_id}_filled.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            # Fill the PDF form
            missing_fields = fill_pdf_form(application, output_path)
            
            # Return the file
            response = FileResponse(
                open(output_path, 'rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{application.reference_number}_{template_name}.pdf"'
            return response
            
        except FileNotFoundError as e:
            logger.error(f"PDF template not found: {str(e)}")
            return Response(
                {"error": "PDF template not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            return Response(
                {"error": f"Error generating PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request, application_id):
        """
        Generate a filled PDF form from an Application instance.
        
        Args:
            request: The HTTP request
            application_id: The ID of the Application to generate a PDF for
            
        Returns:
            Response with the path to the generated PDF and a list of missing fields
        """
        # Get the strict mode parameter
        strict_mode = request.query_params.get('strict', 'false').lower() == 'true'
        
        try:
            # Get the application
            try:
                application = Application.objects.get(id=application_id)
            except Application.DoesNotExist:
                return Response(
                    {"error": f"Application with ID {application_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Create the output directory if it doesn't exist
            output_dir = os.path.join(settings.MEDIA_ROOT, 'application_forms')
            os.makedirs(output_dir, exist_ok=True)
            
            # Define the output path
            output_filename = f"{application_id}_filled.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            # Fill the PDF form
            missing_fields = fill_pdf_form(application, output_path)
            
            # If strict mode is enabled and there are missing fields, return an error
            if strict_mode and missing_fields:
                return Response(
                    {"error": "Missing required fields", "missing_fields": missing_fields},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Return the path to the generated PDF and the list of missing fields
            return Response({
                "pdf_path": f"media/application_forms/{output_filename}",
                "missing_fields": missing_fields
            })
            
        except FileNotFoundError as e:
            logger.error(f"PDF template not found: {str(e)}")
            return Response(
                {"error": "PDF template not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            return Response(
                {"error": f"Error generating PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def has_application_permission(self, user, application):
        """
        Check if user has permission to access this application
        """
        # Admin users can access all applications
        if user.is_staff or user.is_superuser:
            return True
        
        # BDMs can access applications assigned to them
        if hasattr(user, 'role') and user.role == 'bdm' and application.bd and application.bd.user == user:
            return True
        
        # Brokers can access their own applications
        if hasattr(user, 'role') and user.role == 'broker' and application.broker and application.broker.user == user:
            return True
        
        # Users can access applications they created
        if application.created_by == user:
            return True
        
        return False
