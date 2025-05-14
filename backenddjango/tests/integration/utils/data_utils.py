"""
Data utilities for integration tests.
"""

import random
import string
import datetime
from typing import Dict, Any, List, Optional, Union
from decimal import Decimal


def random_string(length: int = 10) -> str:
    """
    Generate a random string of the specified length.
    
    Args:
        length: Length of the string
        
    Returns:
        str: Random string
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def random_email() -> str:
    """
    Generate a random email address.
    
    Returns:
        str: Random email address
    """
    username = random_string(8).lower()
    domain = random_string(6).lower()
    return f"{username}@{domain}.com"


def random_phone() -> str:
    """
    Generate a random phone number.
    
    Returns:
        str: Random phone number
    """
    return f"+1{random.randint(2000000000, 9999999999)}"


def random_address() -> Dict[str, str]:
    """
    Generate a random address.
    
    Returns:
        Dict[str, str]: Random address
    """
    street_number = random.randint(1, 9999)
    street_name = f"{random_string(8)} {random.choice(['St', 'Ave', 'Blvd', 'Rd', 'Ln'])}"
    city = random_string(8).capitalize()
    state = random.choice(['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI'])
    zip_code = f"{random.randint(10000, 99999)}"
    
    return {
        'street': f"{street_number} {street_name}",
        'city': city,
        'state': state,
        'zip_code': zip_code,
        'country': 'USA'
    }


def random_date(
    start_date: datetime.date = datetime.date(2000, 1, 1),
    end_date: datetime.date = datetime.date(2025, 12, 31)
) -> datetime.date:
    """
    Generate a random date between start_date and end_date.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        datetime.date: Random date
    """
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + datetime.timedelta(days=random_days)


def random_datetime(
    start_date: datetime.datetime = datetime.datetime(2000, 1, 1),
    end_date: datetime.datetime = datetime.datetime(2025, 12, 31)
) -> datetime.datetime:
    """
    Generate a random datetime between start_date and end_date.
    
    Args:
        start_date: Start datetime
        end_date: End datetime
        
    Returns:
        datetime.datetime: Random datetime
    """
    seconds_between = int((end_date - start_date).total_seconds())
    random_seconds = random.randint(0, seconds_between)
    return start_date + datetime.timedelta(seconds=random_seconds)


def random_decimal(min_value: float = 0.0, max_value: float = 1000.0, decimal_places: int = 2) -> Decimal:
    """
    Generate a random decimal between min_value and max_value.
    
    Args:
        min_value: Minimum value
        max_value: Maximum value
        decimal_places: Number of decimal places
        
    Returns:
        Decimal: Random decimal
    """
    value = random.uniform(min_value, max_value)
    return Decimal(str(round(value, decimal_places)))


def random_boolean() -> bool:
    """
    Generate a random boolean value.
    
    Returns:
        bool: Random boolean
    """
    return random.choice([True, False])


def random_choice(choices: List[Any]) -> Any:
    """
    Choose a random item from a list.
    
    Args:
        choices: List of choices
        
    Returns:
        Any: Random choice
    """
    return random.choice(choices)


def random_sample(population: List[Any], k: int) -> List[Any]:
    """
    Choose k random items from a population.
    
    Args:
        population: Population to sample from
        k: Number of items to choose
        
    Returns:
        List[Any]: Random sample
    """
    return random.sample(population, k)


def random_dict(keys: List[str], value_generator: callable = random_string) -> Dict[str, Any]:
    """
    Generate a random dictionary with the specified keys.
    
    Args:
        keys: Keys for the dictionary
        value_generator: Function to generate values
        
    Returns:
        Dict[str, Any]: Random dictionary
    """
    return {key: value_generator() for key in keys}


def random_list(length: int, item_generator: callable = random_string) -> List[Any]:
    """
    Generate a random list of the specified length.
    
    Args:
        length: Length of the list
        item_generator: Function to generate items
        
    Returns:
        List[Any]: Random list
    """
    return [item_generator() for _ in range(length)]


def generate_user_data(
    role: str = 'admin',
    is_superuser: bool = True,
    is_staff: bool = True
) -> Dict[str, Any]:
    """
    Generate random user data.
    
    Args:
        role: User role
        is_superuser: Whether the user is a superuser
        is_staff: Whether the user is staff
        
    Returns:
        Dict[str, Any]: User data
    """
    first_name = random_string(8).capitalize()
    last_name = random_string(8).capitalize()
    username = f"{first_name.lower()}.{last_name.lower()}"
    
    return {
        'username': username,
        'email': f"{username}@example.com",
        'password': random_string(12),
        'first_name': first_name,
        'last_name': last_name,
        'role': role,
        'is_superuser': is_superuser,
        'is_staff': is_staff,
        'is_active': True
    }


def generate_borrower_data() -> Dict[str, Any]:
    """
    Generate random borrower data.
    
    Returns:
        Dict[str, Any]: Borrower data
    """
    first_name = random_string(8).capitalize()
    last_name = random_string(8).capitalize()
    address = random_address()
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': f"{first_name.lower()}.{last_name.lower()}@example.com",
        'phone': random_phone(),
        'date_of_birth': random_date(
            start_date=datetime.date(1950, 1, 1),
            end_date=datetime.date(2000, 12, 31)
        ).isoformat(),
        'residential_address': address['street'],
        'residential_city': address['city'],
        'residential_state': address['state'],
        'residential_zip': address['zip_code'],
        'employment_status': random_choice(['Employed', 'Self-Employed', 'Unemployed', 'Retired']),
        'employer_name': random_string(10).capitalize(),
        'annual_income': float(random_decimal(30000, 200000, 2))
    }


def generate_application_data() -> Dict[str, Any]:
    """
    Generate random application data.
    
    Returns:
        Dict[str, Any]: Application data
    """
    return {
        'loan_amount': float(random_decimal(10000, 500000, 2)),
        'loan_purpose': random_choice(['Purchase', 'Refinance', 'Construction', 'Investment']),
        'loan_term': random_choice([12, 24, 36, 48, 60]),
        'interest_rate': float(random_decimal(2.0, 8.0, 2)),
        'status': 'draft',
        'property_address': random_address()['street'],
        'property_city': random_address()['city'],
        'property_state': random_address()['state'],
        'property_zip': random_address()['zip_code'],
        'property_type': random_choice(['Single Family', 'Condo', 'Townhouse', 'Multi-Family']),
        'property_value': float(random_decimal(100000, 1000000, 2))
    }
