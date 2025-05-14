from django.db import transaction
from .models import Borrower, Guarantor, Asset, Liability


def create_borrower_with_financials(borrower_data, assets_data=None, liabilities_data=None, user=None):
    """
    Create a borrower with associated financial information
    
    Args:
        borrower_data: Dictionary containing borrower information
        assets_data: List of dictionaries containing asset information
        liabilities_data: List of dictionaries containing liability information
        user: User creating the borrower
        
    Returns:
        Created Borrower object
    """
    with transaction.atomic():
        # Set created_by if user is provided
        if user:
            borrower_data['created_by'] = user
        
        # Create borrower
        borrower = Borrower.objects.create(**borrower_data)
        
        # Create assets
        if assets_data:
            for asset_data in assets_data:
                asset_data['borrower'] = borrower
                if user:
                    asset_data['created_by'] = user
                Asset.objects.create(**asset_data)
        
        # Create liabilities
        if liabilities_data:
            for liability_data in liabilities_data:
                liability_data['borrower'] = borrower
                if user:
                    liability_data['created_by'] = user
                Liability.objects.create(**liability_data)
        
        return borrower


def create_guarantor_for_application(guarantor_data, borrower_id, application_id, user=None):
    """
    Create a guarantor for a specific borrower and application
    
    Args:
        guarantor_data: Dictionary containing guarantor information
        borrower_id: ID of the borrower
        application_id: ID of the application
        user: User creating the guarantor
        
    Returns:
        Created Guarantor object or None if borrower/application not found
    """
    from applications.models import Application
    
    try:
        borrower = Borrower.objects.get(id=borrower_id)
        application = Application.objects.get(id=application_id)
    except (Borrower.DoesNotExist, Application.DoesNotExist):
        return None
    
    # Set relationships
    guarantor_data['borrower'] = borrower
    guarantor_data['application'] = application
    
    # Set created_by if user is provided
    if user:
        guarantor_data['created_by'] = user
    
    # Create guarantor
    guarantor = Guarantor.objects.create(**guarantor_data)
    
    return guarantor


def get_borrower_financial_summary(borrower_id):
    """
    Get a summary of a borrower's financial situation
    
    Args:
        borrower_id: ID of the borrower
        
    Returns:
        Dictionary with financial summary or None if borrower not found
    """
    try:
        borrower = Borrower.objects.get(id=borrower_id)
    except Borrower.DoesNotExist:
        return None
    
    # Calculate total assets
    assets = borrower.assets.all()
    total_assets = sum(asset.value for asset in assets)
    
    # Calculate total liabilities
    liabilities = borrower.liabilities.all()
    total_liabilities = sum(liability.amount for liability in liabilities)
    
    # Calculate net worth
    net_worth = total_assets - total_liabilities
    
    # Calculate monthly income and expenses
    monthly_income = (borrower.annual_income or 0) / 12
    if borrower.other_income:
        monthly_income += borrower.other_income
    
    monthly_expenses = borrower.monthly_expenses or 0
    
    # Add monthly liability payments
    monthly_liability_payments = sum(
        liability.monthly_payment or 0 
        for liability in liabilities
    )
    
    total_monthly_expenses = monthly_expenses + monthly_liability_payments
    
    # Calculate disposable income
    disposable_income = monthly_income - total_monthly_expenses
    
    return {
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'net_worth': net_worth,
        'monthly_income': monthly_income,
        'monthly_expenses': total_monthly_expenses,
        'disposable_income': disposable_income,
        'asset_breakdown': [
            {
                'type': asset.get_asset_type_display(),
                'value': asset.value,
                'description': asset.description
            }
            for asset in assets
        ],
        'liability_breakdown': [
            {
                'type': liability.get_liability_type_display(),
                'amount': liability.amount,
                'monthly_payment': liability.monthly_payment,
                'description': liability.description
            }
            for liability in liabilities
        ]
    }
