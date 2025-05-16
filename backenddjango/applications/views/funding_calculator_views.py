from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from ..serializers import ManualFundingCalculationSerializer
from ..services import calculate_funding_manual
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class ManualFundingCalculationView(views.APIView):
    """
    API endpoint for manual funding calculations without an application
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=ManualFundingCalculationSerializer,
        responses={200: dict},
        description="Calculate funding based on manually provided parameters",
        examples=[
            OpenApiExample(
                'Example Request',
                value={
                    "loan_amount": 500000,
                    "interest_rate": 5.5,
                    "security_value": 750000,
                    "establishment_fee_rate": 2.5,
                    "capped_interest_months": 9,
                    "monthly_line_fee_rate": 0.25,
                    "brokerage_fee_rate": 1.0,
                    "application_fee": 500,
                    "due_diligence_fee": 1000,
                    "legal_fee_before_gst": 2000,
                    "valuation_fee": 800,
                    "monthly_account_fee": 50,
                    "working_fee": 0
                }
            )
        ]
    )
    def post(self, request, format=None):
        """
        Calculate funding based on manually provided parameters
        """
        serializer = ManualFundingCalculationSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Extract application parameters
                loan_amount = serializer.validated_data.get('loan_amount')
                interest_rate = serializer.validated_data.get('interest_rate')
                security_value = serializer.validated_data.get('security_value')
                
                # Extract calculation input parameters
                calculation_input = {
                    'establishment_fee_rate': serializer.validated_data.get('establishment_fee_rate'),
                    'capped_interest_months': serializer.validated_data.get('capped_interest_months', 9),
                    'monthly_line_fee_rate': serializer.validated_data.get('monthly_line_fee_rate'),
                    'brokerage_fee_rate': serializer.validated_data.get('brokerage_fee_rate'),
                    'application_fee': serializer.validated_data.get('application_fee'),
                    'due_diligence_fee': serializer.validated_data.get('due_diligence_fee'),
                    'legal_fee_before_gst': serializer.validated_data.get('legal_fee_before_gst'),
                    'valuation_fee': serializer.validated_data.get('valuation_fee'),
                    'monthly_account_fee': serializer.validated_data.get('monthly_account_fee'),
                    'working_fee': serializer.validated_data.get('working_fee', 0),
                }
                
                # Perform the calculation
                calculation_result = calculate_funding_manual(
                    loan_amount=loan_amount,
                    interest_rate=interest_rate,
                    security_value=security_value,
                    calculation_input=calculation_input
                )
                
                return Response({
                    "message": "Manual funding calculation completed successfully",
                    "result": calculation_result,
                    "inputs": {
                        "loan_amount": float(loan_amount),
                        "interest_rate": float(interest_rate),
                        "security_value": float(security_value),
                        **{k: float(v) if isinstance(v, (int, float, complex)) else v for k, v in calculation_input.items()}
                    }
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
