import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName
from django.conf import settings
from ..models import Application

logger = logging.getLogger(__name__)

# CORRECTED FIELD MAPPING BASED ON MANUAL PDF EXAMINATION
# This mapping is based on the user's detailed analysis of the actual PDF form fields

# TEXT FIELD MAPPINGS - Based on actual PDF field names and meanings
FIELD_MAP = {
    # SECTION 1: COMPANY BORROWER DETAILS
    "company_name": "Text1",                       # Company Name
    "company_abn_acn": "Text2",                    # ABN/ACN
    "company_industry_type": "Text3",              # Industry Type
    "company_contact_number": "Text4",             # Contact Number
    "annual_company_income": "Text5",              # Annual Company Income ($)
    "trustee_name": "Text6",                       # Trustee Name (if applicable)
    
    # Director 1 Details
    "director1_name": "Text7",                     # Director 1 → Full Name
    "director1_id_1": "Text8",                     # Director 1 → Director ID (digit 1)
    "director1_id_2": "Text9",                     # Director 1 → Director ID (digit 2)
    "director1_id_3": "Text10",                    # Director 1 → Director ID (digit 3)
    "director1_id_4": "Text11",                    # Director 1 → Director ID (digit 4)
    "director1_id_5": "Text12",                    # Director 1 → Director ID (digit 5)
    "director1_id_6": "Text13",                    # Director 1 → Director ID (digit 6)
    "director1_id_7": "Text14",                    # Director 1 → Director ID (digit 7)
    "director1_id_8": "Text15",                    # Director 1 → Director ID (digit 8)
    "director1_id_9": "Text16",                    # Director 1 → Director ID (digit 9)
    "director1_id_10": "Text17",                   # Director 1 → Director ID (digit 10)
    "director1_id_11": "Text18",                   # Director 1 → Director ID (digit 11)
    "director1_id_12": "Text19",                   # Director 1 → Director ID (digit 12)
    
    # Director 2 Details
    "director2_name": "Text30",                    # Director 2 → Full Name
    "director2_id_1": "Text31",                    # Director 2 → Director ID (digit 1)
    "director2_id_2": "Text32",                    # Director 2 → Director ID (digit 2)
    "director2_id_3": "Text33",                    # Director 2 → Director ID (digit 3)
    "director2_id_4": "Text34",                    # Director 2 → Director ID (digit 4)
    "director2_id_5": "Text35",                    # Director 2 → Director ID (digit 5)
    "director2_id_6": "Text36",                    # Director 2 → Director ID (digit 6)
    "director2_id_7": "Text37",                    # Director 2 → Director ID (digit 7)
    "director2_id_8": "Text38",                    # Director 2 → Director ID (digit 8)
    "director2_id_9": "Text39",                    # Director 2 → Director ID (digit 9)
    "director2_id_10": "Text40",                   # Director 2 → Director ID (digit 10)
    "director2_id_11": "Text41",                   # Director 2 → Director ID (digit 11)
    "director2_id_12": "Text42",                   # Director 2 → Director ID (digit 12)
    
    # Registered Business Address
    "company_address_unit": "Text43",              # Unit No.
    "company_address_street_no": "Text44",         # Street No.
    "company_address_street_name": "Text45",       # Street Name
    "company_address_suburb": "Text46",            # Suburb
    "company_address_state": "Text47",             # State
    "company_address_postcode": "Text48",          # Postcode
    
    # SECTION 2: COMPANY ASSETS & LIABILITIES
    # Properties (up to 4)
    "company_property1_address": "Text49",         # Property 1 → Address
    "company_property1_value": "Text50",           # Property 1 → Value ($)
    "company_property1_owing": "Text51",           # Property 1 → Amount Owing ($)
    "company_property2_address": "Text53",         # Property 2 → Address
    "company_property2_value": "Text54",           # Property 2 → Value ($)
    "company_property2_owing": "Text55",           # Property 2 → Amount Owing ($)
    "company_property3_address": "Text59",         # Property 3 → Address
    "company_property3_value": "Text60",           # Property 3 → Value ($)
    "company_property3_owing": "Text61",           # Property 3 → Amount Owing ($)
    "company_property4_address": "Text62",         # Property 4 → Address
    "company_property4_value": "Text63",           # Property 4 → Value ($)
    "company_property4_owing": "Text64",           # Property 4 → Amount Owing ($)
    
    # Other Assets & Liabilities
    "company_vehicles_value": "Text65",            # Vehicle(s) → Value ($)
    "company_vehicles_owing": "Text66",            # Vehicle(s) → Amount Owing ($)
    "company_savings_value": "Text67",             # Savings → Value ($)
    "company_savings_owing": "Text68",             # Savings → Amount Owing ($)
    "company_shares_value": "Text69",              # Investment Shares → Value ($)
    "company_shares_owing": "Text70",              # Investment Shares → Amount Owing ($)
    "company_creditcard_value": "Text71",          # Credit Card(s) → Value ($)
    "company_creditcard_owing": "Text72",          # Credit Card(s) → Amount Owing ($)
    "company_othercreditor_value": "Text73",       # Other Creditor(s) → Value ($)
    "company_othercreditor_owing": "Text74",       # Other Creditor(s) → Amount Owing ($)
    "company_other_value": "Text75",               # Other → Value ($)
    "company_other_owing": "Text76",               # Other → Amount Owing ($)
    
    # Company Asset Totals
    "company_total_assets": "Text77",              # Total Value of Assets ($)
    "company_total_owing": "Text78",               # Total Amount Owing ($)
    
    # SECTION 4: INDIVIDUAL DETAILS (Borrower/Guarantor 1)
    "borrower1_title": "Text106",                  # Title
    "borrower1_given_names": "Text107",            # Given Names
    "borrower1_surname": "Text108",                # Surname
    "borrower1_dob_day": "Text109",                # Date of Birth → Day
    "borrower1_dob_month": "Text110",              # Date of Birth → Month
    "borrower1_dob_year": "Text111",               # Date of Birth → Year
    "borrower1_licence": "Text112",                # Driver's Licence Number
    "borrower1_phone": "Text113",                  # Phone Number – Home
    "borrower1_mobile": "Text114",                 # Mobile Number
    "borrower1_email": "Text115",                  # Email Address
    "borrower1_address_unit": "Text116",           # Residential Address → Unit No.
    "borrower1_address_street_no": "Text117",      # Residential Address → Street No.
    "borrower1_address_street_name": "Text118",    # Residential Address → Street Name
    "borrower1_address_suburb": "Text119",         # Residential Address → Suburb
    "borrower1_address_state": "Text120",          # Residential Address → State
    "borrower1_address_postcode": "Text121",       # Residential Address → Postcode
    "borrower1_occupation": "Text122",             # Employment → Occupation
    "borrower1_employer": "Text123",               # Employer Name / Trading Name
    "borrower1_annual_income": "Text128",          # Annual Income (before tax)
    
    # SECTION 4: INDIVIDUAL DETAILS (Borrower/Guarantor 2)
    "borrower2_title": "Text129",                  # Title
    "borrower2_given_names": "Text130",            # Given Names
    "borrower2_surname": "Text131",                # Surname
    "borrower2_dob_day": "Text132",                # Date of Birth → Day
    "borrower2_dob_month": "Text133",              # Date of Birth → Month
    "borrower2_dob_year": "Text134",               # Date of Birth → Year
    "borrower2_licence": "Text135",                # Driver's Licence Number
    "borrower2_phone": "Text136",                  # Phone Number – Home
    "borrower2_mobile": "Text137",                 # Mobile Number
    "borrower2_email": "Text138",                  # Email Address
    "borrower2_address_unit": "Text139",           # Residential Address → Unit No.
    "borrower2_address_street_no": "Text140",      # Residential Address → Street No.
    "borrower2_address_street_name": "Text141",    # Residential Address → Street Name
    "borrower2_address_suburb": "Text142",         # Residential Address → Suburb
    "borrower2_address_state": "Text143",          # Residential Address → State
    "borrower2_address_postcode": "Text144",       # Residential Address → Postcode
    "borrower2_occupation": "Text145",             # Employment → Occupation
    "borrower2_employer": "Text146",               # Employer Name / Trading Name
    "borrower2_annual_income": "Text151",          # Annual Income (before tax)
    
    # SECTION 5: GUARANTOR ASSETS & LIABILITIES
    # Property Assets
    "guarantor_property1_address": "Text152",      # Property 1 → Address
    "guarantor_property1_value": "Text153",        # Property 1 → Value ($)
    "guarantor_property1_owing": "Text154",        # Property 1 → Amount Owing ($)
    "guarantor_property2_address": "Text157",      # Property 2 → Address
    "guarantor_property2_value": "Text158",        # Property 2 → Value ($)
    "guarantor_property2_owing": "Text159",        # Property 2 → Amount Owing ($)
    "guarantor_property3_address": "Text160",      # Property 3 → Address
    "guarantor_property3_value": "Text161",        # Property 3 → Value ($)
    "guarantor_property3_owing": "Text162",        # Property 3 → Amount Owing ($)
    "guarantor_property4_address": "Text163",      # Property 4 → Address
    "guarantor_property4_value": "Text164",        # Property 4 → Value ($)
    "guarantor_property4_owing": "Text165",        # Property 4 → Amount Owing ($)
    
    # Other Guarantor Assets & Liabilities
    "guarantor_vehicles_value": "Text166",         # Vehicle(s) → Value ($)
    "guarantor_vehicles_owing": "Text167",         # Vehicle(s) → Amount Owing ($)
    "guarantor_savings_value": "Text168",          # Savings → Value ($)
    "guarantor_savings_owing": "Text169",          # Savings → Amount Owing ($)
    "guarantor_shares_value": "Text170",           # Investment Shares → Value ($)
    "guarantor_shares_owing": "Text171",           # Investment Shares → Amount Owing ($)
    "guarantor_creditcard_value": "Text172",       # Credit Card(s) → Value ($)
    "guarantor_creditcard_owing": "Text173",       # Credit Card(s) → Amount Owing ($)
    "guarantor_othercreditor_value": "Text174",    # Other Creditor(s) → Value ($)
    "guarantor_othercreditor_owing": "Text175",    # Other Creditor(s) → Amount Owing ($)
    "guarantor_other_value": "Text176",            # Other → Value ($)
    "guarantor_other_owing": "Text177",            # Other → Amount Owing ($)
    
    # Guarantor Asset Totals
    "guarantor_total_assets": "Text178",           # Total Value of All Assets ($)
    "guarantor_total_owing": "Text179",            # Total Amount Owing on All Assets ($)
    
    # SECTION 6: PROPOSED SECURITY DETAILS - PROPERTY 1
    "security1_unit": "Text198",                   # Unit No.
    "security1_street_no": "Text199",              # Street No.
    "security1_street_name": "Text200",            # Street Name
    "security1_suburb": "Text201",                 # Suburb
    "security1_state": "Text202",                  # State
    "security1_postcode": "Text203",               # Postcode
    "security1_mortgagee1": "Text204",             # Current Mortgagee Name – 1st Mortgage
    "security1_mortgagee2": "Text205",             # Current Mortgagee Name – 2nd Mortgage
    "security1_debt1": "Text206",                  # Current Debt Position – 1st Mortgage Amount
    "security1_debt2": "Text207",                  # Current Debt Position – 2nd Mortgage Amount
    "security1_current_value": "Text210",          # Est. Current Value – Value ($)
    "security1_purchase_price": "Text211",         # Purchase Price – Value ($)
    "security1_type_other": "Text218",             # If Other, specify
    "security1_bedrooms": "Text219",               # No. of Bedrooms
    "security1_bathrooms": "Text220",              # No. of Bathrooms
    "security1_car_spaces": "Text221",             # No. of Car Spaces
    "security1_building_size": "Text222",          # Building Size (sqm)
    "security1_land_size": "Text223",              # Land Size (sqm)
    
    # SECTION 6: PROPOSED SECURITY DETAILS - PROPERTY 2
    "security2_unit": "Text231",                   # Unit No.
    "security2_street_no": "Text232",              # Street No.
    "security2_street_name": "Text233",            # Street Name
    "security2_suburb": "Text234",                 # Suburb
    "security2_state": "Text235",                  # State
    "security2_postcode": "Text236",               # Postcode
    "security2_mortgagee1": "Text237",             # 1st Mortgage – Lender Name
    "security2_mortgagee2": "Text238",             # 2nd Mortgage – Lender Name
    "security2_debt1": "Text239",                  # 1st Mortgage – Amount ($)
    "security2_debt2": "Text240",                  # 2nd Mortgage – Amount ($)
    "security2_current_value": "Text243",          # Est. Current Value – Value ($)
    "security2_purchase_price": "Text244",         # Purchase Price – Value ($)
    "security2_type_other": "Text251",             # If Other, please specify
    "security2_bedrooms": "Text252",               # Bedrooms
    "security2_bathrooms": "Text253",              # Bathrooms
    "security2_car_spaces": "Text254",             # Car Spaces
    "security2_building_size": "Text255",          # Building Size (sqm)
    "security2_land_size": "Text256",              # Land Size (sqm)
    
    # SECTION 6: PROPOSED SECURITY DETAILS - PROPERTY 3
    "security3_unit": "Text264",                   # Unit No.
    "security3_street_no": "Text265",              # Street No.
    "security3_street_name": "Text266",            # Street Name
    "security3_suburb": "Text267",                 # Suburb
    "security3_state": "Text268",                  # State
    "security3_postcode": "Text269",               # Postcode
    "security3_mortgagee1": "Text270",             # 1st Mortgage – Lender Name
    "security3_mortgagee2": "Text271",             # 2nd Mortgage – Lender Name
    "security3_debt1": "Text272",                  # 1st Mortgage – Amount ($)
    "security3_debt2": "Text273",                  # 2nd Mortgage – Amount ($)
    "security3_current_value": "Text276",          # Est. Current Value – Value ($)
    "security3_purchase_price": "Text277",         # Purchase Price – Value ($)
    "security3_type_other": "Text284",             # If Other, please specify
    "security3_bedrooms": "Text285",               # Bedrooms
    "security3_bathrooms": "Text286",              # Bathrooms
    "security3_car_spaces": "Text287",             # Car Spaces
    "security3_building_size": "Text288",          # Building Size (sqm)
    "security3_land_size": "Text289",              # Land Size (sqm)
    
    # SECTION 7: LOAN DETAILS & PURPOSE
    "loan_amount": "Text297",                      # Net Loan Required ($)
    "loan_term": "Text298",                        # Term Required (Months)
    "settlement_date_day": "Text299",              # Proposed Settlement Date – Day
    "settlement_date_month": "Text300",            # Proposed Settlement Date – Month
    "settlement_date_year": "Text301",             # Proposed Settlement Date – Year
    "expected_rate": "Text302",                    # Expected Rate (p.a.) (%)
    "additional_comments": "Text312",              # Additional Comments
    "other_submissions_details": "Text315",        # If yes, provide details
    
    # SECTION 8: LOAN REQUIREMENTS
    "loan_purpose1_desc": "Text316",               # Purpose Line 1 – Description
    "loan_purpose1_amount": "Text317",             # Purpose Line 1 – Amount ($)
    "loan_purpose2_desc": "Text318",               # Purpose Line 2 – Description
    "loan_purpose2_amount": "Text319",             # Purpose Line 2 – Amount ($)
    "loan_purpose3_desc": "Text320",               # Purpose Line 3 – Description
    "loan_purpose3_amount": "Text321",             # Purpose Line 3 – Amount ($)
    "loan_purpose4_desc": "Text322",               # Purpose Line 4 – Description
    "loan_purpose4_amount": "Text323",             # Purpose Line 4 – Amount ($)
    "loan_purpose5_desc": "Text324",               # Purpose Line 5 – Description
    "loan_purpose5_amount": "Text325",             # Purpose Line 5 – Amount ($)
    "loan_purpose6_desc": "Text326",               # Purpose Line 6 – Description
    "loan_purpose6_amount": "Text327",             # Purpose Line 6 – Amount ($)
    "loan_purposes_total": "Text328",              # Total Amount ($) of All Loan Purposes
    
    # SECTION 9: PROPOSED EXIT STRATEGY
    "exit_strategy_other_details": "Text333",      # If "Other" is selected, specify details
}

# CHECKBOX FIELD MAPPINGS - Based on actual PDF checkbox names
CHECKBOX_MAP = {
    # SECTION 1: COMPANY BORROWER DETAILS
    "is_trustee_yes": "Check Box20",               # Is the Company a Trustee? → Yes
    "is_trustee_no": "Check Box21",                # Is the Company a Trustee? → No
    "is_smsf_trustee_yes": "Check Box22",          # Is the Company a Trustee for an SMSF? → Yes
    "is_smsf_trustee_no": "Check Box23",           # Is the Company a Trustee for an SMSF? → No
    
    # Director 1 Roles
    "director1_role_director": "Check Box24",      # Director 1 Role → Director
    "director1_role_secretary": "Check Box25",     # Director 1 Role → Secretary
    "director1_role_public_officer": "Check Box26", # Director 1 Role → Public Officer
    
    # Director 2 Roles
    "director2_role_director": "Check Box27",      # Director 2 Role → Director
    "director2_role_secretary": "Check Box28",     # Director 2 Role → Secretary
    "director2_role_public_officer": "Check Box29", # Director 2 Role → Public Officer
    
    # SECTION 2: COMPANY ASSETS & LIABILITIES
    "company_property1_refinance": "Check Box52", # Property 1 → To be refinanced
    "company_property2_refinance": "Check Box83", # Property 2 → To be refinanced
    "company_property3_refinance": "Check Box84", # Property 3 → To be refinanced
    "company_property4_refinance": "Check Box85", # Property 4 → To be refinanced
    "company_vehicles_refinance": "Check Box86",  # Vehicle(s) → To be refinanced
    "company_savings_refinance": "Check Box87",   # Savings → To be refinanced
    "company_shares_refinance": "Check Box88",    # Investment Shares → To be refinanced
    "company_creditcard_refinance": "Check Box89", # Credit Card(s) → To be refinanced
    "company_othercreditor_refinance": "Check Box90", # Other Creditor(s) → To be refinanced
    "company_other_refinance": "Check Box91",     # Other → To be refinanced
    
    # SECTION 3: GENERAL SOLVENCY ENQUIRIES
    "pending_litigation_yes": "Check Box92",      # Q1: Pending/past litigation? → Yes
    "pending_litigation_no": "Check Box93",       # Q1: Pending/past litigation? → No
    "unsatisfied_judgements_yes": "Check Box94",  # Q2: Unsatisfied judgements? → Yes
    "unsatisfied_judgements_no": "Check Box95",   # Q2: Unsatisfied judgements? → No
    "been_bankrupt_yes": "Check Box96",           # Q3: Been bankrupt/insolvent? → Yes
    "been_bankrupt_no": "Check Box97",            # Q3: Been bankrupt/insolvent? → No
    "refused_credit_yes": "Check Box98",          # Q4: Been refused credit? → Yes
    "refused_credit_no": "Check Box99",           # Q4: Been refused credit? → No
    "ato_debt_yes": "Check Box100",               # Q5: Outstanding ATO debts? → Yes
    "ato_debt_no": "Check Box101",                # Q5: Outstanding ATO debts? → No
    "tax_returns_yes": "Check Box102",            # Q6: Outstanding Tax/BAS returns? → Yes
    "tax_returns_no": "Check Box103",             # Q6: Outstanding Tax/BAS returns? → No
    "payment_arrangements_yes": "Check Box104",   # Q7: Payment arrangement with creditor? → Yes
    "payment_arrangements_no": "Check Box105",    # Q7: Payment arrangement with creditor? → No
    
    # SECTION 4: INDIVIDUAL DETAILS - Employment Types
    # Borrower/Guarantor 1
    "borrower1_fulltime": "Check Box124",         # Employment Type → Full Time
    "borrower1_parttime": "Check Box125",         # Employment Type → Part Time
    "borrower1_casual": "Check Box126",           # Employment Type → Casual / Temporary
    "borrower1_contract": "Check Box127",         # Employment Type → Contract
    
    # Borrower/Guarantor 2
    "borrower2_fulltime": "Check Box147",         # Employment Type → Full Time
    "borrower2_parttime": "Check Box148",         # Employment Type → Part Time
    "borrower2_casual": "Check Box149",           # Employment Type → Casual / Temporary
    "borrower2_contract": "Check Box150",         # Employment Type → Contract
    
    # SECTION 5: GUARANTOR ASSETS & LIABILITIES - B/G1 or B/G2 Attribution
    # Property Assets
    "guarantor_property1_bg1": "Check Box155",    # Property 1 → B/G1
    "guarantor_property1_bg2": "Check Box156",    # Property 1 → B/G2
    "guarantor_property2_bg1": "Check Box180",    # Property 2 → B/G1
    "guarantor_property2_bg2": "Check Box181",    # Property 2 → B/G2
    "guarantor_property3_bg1": "Check Box182",    # Property 3 → B/G1
    "guarantor_property3_bg2": "Check Box183",    # Property 3 → B/G2
    "guarantor_property4_bg1": "Check Box184",    # Property 4 → B/G1
    "guarantor_property4_bg2": "Check Box185",    # Property 4 → B/G2
    
    # Other Asset & Liability Types
    "guarantor_vehicles_bg1": "Check Box186",     # Vehicle(s) → B/G1
    "guarantor_vehicles_bg2": "Check Box187",     # Vehicle(s) → B/G2
    "guarantor_savings_bg1": "Check Box188",      # Savings → B/G1
    "guarantor_savings_bg2": "Check Box189",      # Savings → B/G2
    "guarantor_shares_bg1": "Check Box190",       # Investment Shares → B/G1
    "guarantor_shares_bg2": "Check Box191",       # Investment Shares → B/G2
    "guarantor_creditcard_bg1": "Check Box192",   # Credit Card(s) → B/G1
    "guarantor_creditcard_bg2": "Check Box193",   # Credit Card(s) → B/G2
    "guarantor_othercreditor_bg1": "Check Box194", # Other Creditor(s) → B/G1
    "guarantor_othercreditor_bg2": "Check Box195", # Other Creditor(s) → B/G2
    "guarantor_other_bg1": "Check Box196",        # Other → B/G1
    "guarantor_other_bg2": "Check Box197",        # Other → B/G2
    
    # SECTION 6: PROPOSED SECURITY DETAILS - PROPERTY 1
    "security1_valuation_current": "Check Box208", # Valuation → Est. Current Value (tick)
    "security1_valuation_purchase": "Check Box209", # Valuation → Purchase Price (tick)
    
    # Property Type
    "security1_residential": "Check Box212",      # Residential
    "security1_commercial": "Check Box213",       # Commercial
    "security1_rural": "Check Box214",            # Rural
    "security1_industrial": "Check Box215",       # Industrial
    "security1_vacant_land": "Check Box216",      # Vacant Land
    "security1_other": "Check Box217",            # Other (Please Specify)
    
    # Property Features
    "security1_single_story": "Check Box224",     # Single Story
    "security1_double_story": "Check Box225",     # Double Story
    "security1_garage": "Check Box226",           # Garage
    "security1_carport": "Check Box227",          # Carport
    "security1_off_street": "Check Box228",       # Off-Street
    
    # Owner Type
    "security1_owner_occupied": "Check Box229",   # Owner Occupied
    "security1_investment": "Check Box230",       # Investment Property
    
    # SECTION 6: PROPOSED SECURITY DETAILS - PROPERTY 2
    "security2_valuation_current": "Check Box241", # Valuation → Est. Current Value (tick)
    "security2_valuation_purchase": "Check Box243", # Valuation → Purchase Price (tick)
    
    # Property Type
    "security2_residential": "Check Box245",      # Residential
    "security2_commercial": "Check Box246",       # Commercial
    "security2_rural": "Check Box247",            # Rural
    "security2_industrial": "Check Box248",       # Industrial
    "security2_vacant_land": "Check Box249",      # Vacant Land
    "security2_other": "Check Box250",            # Other (Please Specify)
    
    # Property Features
    "security2_single_story": "Check Box257",     # Single Story
    "security2_double_story": "Check Box258",     # Double Story
    "security2_garage": "Check Box259",           # Garage
    "security2_carport": "Check Box260",          # Carport
    "security2_off_street": "Check Box261",       # Off-Street
    
    # Occupancy Status
    "security2_owner_occupied": "Check Box262",   # Owner Occupied
    "security2_investment": "Check Box263",       # Investment Property
    
    # SECTION 6: PROPOSED SECURITY DETAILS - PROPERTY 3
    "security3_valuation_current": "Check Box274", # Valuation → Est. Current Value (tick)
    "security3_valuation_purchase": "Check Box275", # Valuation → Purchase Price (tick)
    
    # Property Type
    "security3_residential": "Check Box278",      # Residential
    "security3_commercial": "Check Box279",       # Commercial
    "security3_rural": "Check Box280",            # Rural
    "security3_industrial": "Check Box281",       # Industrial
    "security3_vacant_land": "Check Box282",      # Vacant Land
    "security3_other": "Check Box283",            # Other
    
    # Building Features
    "security3_single_story": "Check Box290",     # Single Story
    "security3_double_story": "Check Box291",     # Double Story
    "security3_garage": "Check Box292",           # Garage
    "security3_carport": "Check Box293",          # Carport
    "security3_off_street": "Check Box294",       # Off-Street
    
    # Occupancy Status
    "security3_owner_occupied": "Check Box295",   # Owner Occupied
    "security3_investment": "Check Box296",       # Investment Property
    
    # SECTION 7: LOAN DETAILS & PURPOSE
    # Loan Purpose
    "loan_purpose_purchase": "Check Box303",      # Loan Purpose → Purchase
    "loan_purpose_seed_capital": "Check Box304",  # Loan Purpose → Seed Capital
    "loan_purpose_settlement_shortfall": "Check Box305", # Loan Purpose → Settlement Shortfall
    "loan_purpose_equity_venture": "Check Box306", # Loan Purpose → Equity Venture
    "loan_purpose_cash_out": "Check Box307",      # Loan Purpose → Cash Out
    "loan_purpose_refinance": "Check Box308",     # Loan Purpose → Refinance
    "loan_purpose_construction": "Check Box309",  # Loan Purpose → Construction
    "loan_purpose_payout_debt": "Check Box310",   # Loan Purpose → Payout Existing Debt
    "loan_purpose_other": "Check Box311",         # Loan Purpose → Other (specify)
    
    # Disclosure of Other Submissions
    "other_submissions_yes": "Check Box313",      # Has this loan been submitted elsewhere? → Yes
    "other_submissions_no": "Check Box314",       # Has this loan been submitted elsewhere? → No
    
    # SECTION 9: PROPOSED EXIT STRATEGY
    # Finance Takeout Method
    "exit_strategy_refinance": "Check Box329",    # Takeout Method → Refinance
    "exit_strategy_sale": "Check Box330",         # Takeout Method → Sale of Security
    "exit_strategy_cash_flow": "Check Box331",    # Takeout Method → Cash-flow
    "exit_strategy_other": "Check Box332",        # Takeout Method → Other (Please Specify)
}

def fill_pdf_form(application: Application, output_path: str) -> List[str]:
    """
    Fill PDF form with application data using corrected field mappings
    
    Args:
        application: The Application instance to extract data from
        output_path: Path where the filled PDF should be saved
        
    Returns:
        List of field names that couldn't be filled due to missing data
    """
    # Get the template PDF path
    template_path = os.path.join(
        settings.BASE_DIR, 
        "applications", 
        "ApplicationTemplate", 
        "Eternity Capital - Application Form (1).pdf"
    )
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template PDF not found at: {template_path}")
    
    # Extract data from application
    form_data = extract_application_data(application)
    checkbox_data = extract_checkbox_data(application)
    
    logger.info(f"Filling PDF form with data: {form_data}")
    logger.info(f"Filling PDF form with checkbox data: {checkbox_data}")
    
    try:
        # Read the template PDF
        template_pdf = PdfReader(template_path)
        
        # Create a new PDF writer
        writer = PdfWriter()
        
        missing_fields = []
        
        # Process each page
        for page_num, page in enumerate(template_pdf.pages):
            # Get form annotations
            if '/Annots' in page:
                annotations = page['/Annots']
                if annotations:
                    for annotation in annotations:
                        if annotation and '/T' in annotation:
                            field_name = str(annotation['/T']).strip('()/')
                            
                            # Handle text fields
                            if field_name in FIELD_MAP.values():
                                # Find the data key for this field
                                data_key = None
                                for key, pdf_field in FIELD_MAP.items():
                                    if pdf_field == field_name:
                                        data_key = key
                                        break
                                
                                if data_key and data_key in form_data:
                                    value = str(form_data[data_key])
                                    annotation.update(PdfDict(V=value, AS=value))
                                    logger.debug(f"Filling text field {field_name} with value: {value}")
                                else:
                                    logger.debug(f"Missing text field data for {data_key} -> {field_name}")
                                    missing_fields.append(data_key or field_name)
                            
                            # Handle checkbox fields
                            elif field_name in CHECKBOX_MAP.values():
                                # Find the checkbox key for this field
                                checkbox_key = None
                                for key, pdf_field in CHECKBOX_MAP.items():
                                    if pdf_field == field_name:
                                        checkbox_key = key
                                        break
                                
                                if checkbox_key and checkbox_key in checkbox_data:
                                    if checkbox_data[checkbox_key]:
                                        annotation.update(PdfDict(AS=PdfName.Yes, V=PdfName.Yes))
                                        logger.debug(f"Setting checkbox {field_name} to checked")
                                    else:
                                        annotation.update(PdfDict(AS=PdfName.Off, V=PdfName.Off))
                                        logger.debug(f"Setting checkbox {field_name} to unchecked")
            
            # Add the page to writer
            writer.addPage(page)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the filled PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"PDF generated successfully at: {output_path}")
        return missing_fields
        
    except Exception as e:
        logger.error(f"Error filling PDF form: {str(e)}")
        raise


def extract_application_data(application: Application) -> Dict[str, Any]:
    """
    Extract data from Application model and related models for PDF form filling
    Based on corrected field mappings
    """
    data = {}
    
    # Basic loan details
    if application.loan_amount:
        data["loan_amount"] = str(application.loan_amount)
    if application.loan_term:
        data["loan_term"] = str(application.loan_term)
    if application.interest_rate:
        data["expected_rate"] = str(application.interest_rate)
    
    # Settlement date
    if application.estimated_settlement_date:
        settlement_date = application.estimated_settlement_date
        data["settlement_date_day"] = str(settlement_date.day)
        data["settlement_date_month"] = str(settlement_date.month)
        data["settlement_date_year"] = str(settlement_date.year)
    
    # Additional comments
    if application.additional_comments:
        data["additional_comments"] = application.additional_comments
    
    # Get company borrowers
    company_borrowers = application.borrowers.filter(is_company=True)
    if company_borrowers.exists():
        company = company_borrowers.first()
        
        # Basic company info
        if company.company_name:
            data["company_name"] = company.company_name
        if company.company_abn:
            data["company_abn_acn"] = company.company_abn
        elif company.company_acn:
            data["company_abn_acn"] = company.company_acn
        if company.industry_type:
            data["company_industry_type"] = company.industry_type.title()
        if company.contact_number:
            data["company_contact_number"] = company.contact_number
        if company.annual_company_income:
            data["annual_company_income"] = str(company.annual_company_income)
        if company.trustee_name:
            data["trustee_name"] = company.trustee_name
        
        # Company address
        if company.registered_address_unit:
            data["company_address_unit"] = company.registered_address_unit
        if company.registered_address_street_no:
            data["company_address_street_no"] = company.registered_address_street_no
        if company.registered_address_street_name:
            data["company_address_street_name"] = company.registered_address_street_name
        if company.registered_address_suburb:
            data["company_address_suburb"] = company.registered_address_suburb
        if company.registered_address_state:
            data["company_address_state"] = company.registered_address_state
        if company.registered_address_postcode:
            data["company_address_postcode"] = company.registered_address_postcode
        
        # Directors (if available)
        directors = company.directors.all()
        if directors.exists():
            director1 = directors[0] if len(directors) >= 1 else None
            director2 = directors[1] if len(directors) >= 2 else None
            
            if director1:
                data["director1_name"] = director1.name
                if director1.director_id:
                    # Split director ID into individual digits (up to 12 characters)
                    director_id = str(director1.director_id).ljust(12, ' ')
                    for i in range(12):
                        if i < len(director_id) and director_id[i] != ' ':
                            data[f"director1_id_{i+1}"] = director_id[i]
            
            if director2:
                data["director2_name"] = director2.name
                if director2.director_id:
                    # Split director ID into individual digits (up to 12 characters)
                    director_id = str(director2.director_id).ljust(12, ' ')
                    for i in range(12):
                        if i < len(director_id) and director_id[i] != ' ':
                            data[f"director2_id_{i+1}"] = director_id[i]
    
    # Get individual borrowers (up to 2)
    individual_borrowers = application.borrowers.filter(is_company=False)
    borrower_count = 0
    
    for borrower in individual_borrowers[:2]:  # Limit to 2 borrowers
        borrower_count += 1
        prefix = f"borrower{borrower_count}"
        
        # Basic individual info
        if borrower.first_name:
            data[f"{prefix}_given_names"] = borrower.first_name
        if borrower.last_name:
            data[f"{prefix}_surname"] = borrower.last_name
        
        # Date of birth
        if borrower.date_of_birth:
            dob = borrower.date_of_birth
            data[f"{prefix}_dob_day"] = str(dob.day)
            data[f"{prefix}_dob_month"] = str(dob.month)
            data[f"{prefix}_dob_year"] = str(dob.year)
        
        # Contact info
        if borrower.phone:
            data[f"{prefix}_phone"] = borrower.phone
        if borrower.email:
            data[f"{prefix}_email"] = borrower.email
        
        # Address (parse from residential_address)
        if borrower.residential_address:
            # Try to extract components from full address
            address_parts = borrower.residential_address.split(',')
            if len(address_parts) >= 2:
                street_part = address_parts[0].strip()
                # Try to extract unit and street number from street part
                street_words = street_part.split()
                if len(street_words) >= 2:
                    # First word might be unit, second might be street number
                    if street_words[0].lower().startswith(('unit', 'apt', 'level')):
                        data[f"{prefix}_address_unit"] = street_words[1] if len(street_words) > 1 else ""
                        if len(street_words) >= 3:
                            data[f"{prefix}_address_street_no"] = street_words[2]
                            data[f"{prefix}_address_street_name"] = " ".join(street_words[3:])
                    else:
                        # First word is likely street number
                        data[f"{prefix}_address_street_no"] = street_words[0]
                        data[f"{prefix}_address_street_name"] = " ".join(street_words[1:])
                
                # Suburb (usually second part)
                if len(address_parts) >= 2:
                    suburb_state_post = address_parts[1].strip()
                    suburb_words = suburb_state_post.split()
                    if len(suburb_words) >= 3:
                        data[f"{prefix}_address_suburb"] = " ".join(suburb_words[:-2])
                        data[f"{prefix}_address_state"] = suburb_words[-2]
                        data[f"{prefix}_address_postcode"] = suburb_words[-1]
        
        # Employment
        if borrower.job_title:
            data[f"{prefix}_occupation"] = borrower.job_title
        if borrower.employer_name:
            data[f"{prefix}_employer"] = borrower.employer_name
        if borrower.annual_income:
            data[f"{prefix}_annual_income"] = str(borrower.annual_income)
    
    # Get guarantors (treated as additional individuals)
    guarantors = application.guarantors.all()
    if guarantors.exists():
        # For now, map first guarantor to borrower2 if borrower2 slot is available
        if borrower_count < 2 and guarantors.first():
            guarantor = guarantors.first()
            prefix = "borrower2"
            
            if guarantor.title:
                data[f"{prefix}_title"] = guarantor.title.title()
            if guarantor.first_name:
                data[f"{prefix}_given_names"] = guarantor.first_name
            if guarantor.last_name:
                data[f"{prefix}_surname"] = guarantor.last_name
            
            # Date of birth
            if guarantor.date_of_birth:
                dob = guarantor.date_of_birth
                data[f"{prefix}_dob_day"] = str(dob.day)
                data[f"{prefix}_dob_month"] = str(dob.month)
                data[f"{prefix}_dob_year"] = str(dob.year)
            
            # Contact info
            if guarantor.home_phone:
                data[f"{prefix}_phone"] = guarantor.home_phone
            if guarantor.mobile:
                data[f"{prefix}_mobile"] = guarantor.mobile
            if guarantor.email:
                data[f"{prefix}_email"] = guarantor.email
            
            # Address
            if guarantor.address_unit:
                data[f"{prefix}_address_unit"] = guarantor.address_unit
            if guarantor.address_street_no:
                data[f"{prefix}_address_street_no"] = guarantor.address_street_no
            if guarantor.address_street_name:
                data[f"{prefix}_address_street_name"] = guarantor.address_street_name
            if guarantor.address_suburb:
                data[f"{prefix}_address_suburb"] = guarantor.address_suburb
            if guarantor.address_state:
                data[f"{prefix}_address_state"] = guarantor.address_state
            if guarantor.address_postcode:
                data[f"{prefix}_address_postcode"] = guarantor.address_postcode
            
            # Employment
            if guarantor.occupation:
                data[f"{prefix}_occupation"] = guarantor.occupation
            if guarantor.employer_name:
                data[f"{prefix}_employer"] = guarantor.employer_name
            if guarantor.annual_income:
                data[f"{prefix}_annual_income"] = str(guarantor.annual_income)
    
    # Get security properties
    security_properties = application.security_properties.all()
    for i, prop in enumerate(security_properties[:3]):  # Limit to 3 properties
        prop_num = i + 1
        prefix = f"security{prop_num}"
        
        # Address
        if prop.address_unit:
            data[f"{prefix}_unit"] = prop.address_unit
        if prop.address_street_no:
            data[f"{prefix}_street_no"] = prop.address_street_no
        if prop.address_street_name:
            data[f"{prefix}_street_name"] = prop.address_street_name
        if prop.address_suburb:
            data[f"{prefix}_suburb"] = prop.address_suburb
        if prop.address_state:
            data[f"{prefix}_state"] = prop.address_state
        if prop.address_postcode:
            data[f"{prefix}_postcode"] = prop.address_postcode
        
        # Mortgage details
        if prop.current_mortgagee:
            data[f"{prefix}_mortgagee1"] = prop.current_mortgagee
        if prop.first_mortgage:
            data[f"{prefix}_debt1"] = prop.first_mortgage
        if prop.second_mortgage:
            data[f"{prefix}_debt2"] = prop.second_mortgage
        
        # Valuation
        if prop.estimated_value:
            data[f"{prefix}_current_value"] = str(prop.estimated_value)
        if prop.purchase_price:
            data[f"{prefix}_purchase_price"] = str(prop.purchase_price)
        
        # Property details
        if prop.bedrooms:
            data[f"{prefix}_bedrooms"] = str(prop.bedrooms)
        if prop.bathrooms:
            data[f"{prefix}_bathrooms"] = str(prop.bathrooms)
        if prop.car_spaces:
            data[f"{prefix}_car_spaces"] = str(prop.car_spaces)
        if prop.building_size:
            data[f"{prefix}_building_size"] = str(prop.building_size)
        if prop.land_size:
            data[f"{prefix}_land_size"] = str(prop.land_size)
    
    # Get loan requirements
    loan_requirements = application.loan_requirements.all()
    for i, req in enumerate(loan_requirements[:6]):  # Limit to 6 requirements
        req_num = i + 1
        if req.description:
            data[f"loan_purpose{req_num}_desc"] = req.description
        if req.amount:
            data[f"loan_purpose{req_num}_amount"] = str(req.amount)
    
    # Calculate total loan purposes
    total_amount = sum(req.amount for req in loan_requirements if req.amount)
    if total_amount:
        data["loan_purposes_total"] = str(total_amount)
    
    return data


def extract_checkbox_data(application: Application) -> Dict[str, bool]:
    """
    Extract checkbox data from Application model and related models
    Based on corrected checkbox mappings
    """
    data = {}
    
    # Company trustee status
    company_borrowers = application.borrowers.filter(is_company=True)
    if company_borrowers.exists():
        company = company_borrowers.first()
        
        # Trustee checkboxes
        if company.is_trustee is not None:
            data["is_trustee_yes"] = company.is_trustee
            data["is_trustee_no"] = not company.is_trustee
        
        if company.is_smsf_trustee is not None:
            data["is_smsf_trustee_yes"] = company.is_smsf_trustee
            data["is_smsf_trustee_no"] = not company.is_smsf_trustee
        
        # Director roles (if available)
        directors = company.directors.all()
        if directors.exists():
            director1 = directors[0] if len(directors) >= 1 else None
            director2 = directors[1] if len(directors) >= 2 else None
            
            if director1 and director1.roles:
                roles = director1.roles.lower()
                data["director1_role_director"] = "director" in roles
                data["director1_role_secretary"] = "secretary" in roles
                data["director1_role_public_officer"] = "public officer" in roles or "public_officer" in roles
            
            if director2 and director2.roles:
                roles = director2.roles.lower()
                data["director2_role_director"] = "director" in roles
                data["director2_role_secretary"] = "secretary" in roles
                data["director2_role_public_officer"] = "public officer" in roles or "public_officer" in roles
    
    # Employment types for individual borrowers
    individual_borrowers = application.borrowers.filter(is_company=False)
    borrower_count = 0
    
    for borrower in individual_borrowers[:2]:
        borrower_count += 1
        prefix = f"borrower{borrower_count}"
        
        if borrower.employment_type:
            emp_type = borrower.employment_type.lower()
            data[f"{prefix}_fulltime"] = emp_type == "full_time"
            data[f"{prefix}_parttime"] = emp_type == "part_time"
            data[f"{prefix}_casual"] = emp_type == "casual"
            data[f"{prefix}_contract"] = emp_type == "contractor" or emp_type == "contract"
    
    # Employment type for guarantors (if mapped to borrower2)
    guarantors = application.guarantors.all()
    if guarantors.exists() and borrower_count < 2:
        guarantor = guarantors.first()
        if guarantor.employment_type:
            emp_type = guarantor.employment_type.lower()
            data["borrower2_fulltime"] = emp_type == "full_time"
            data["borrower2_parttime"] = emp_type == "part_time"
            data["borrower2_casual"] = emp_type == "casual"
            data["borrower2_contract"] = emp_type == "contract"
    
    # Solvency enquiries
    data["pending_litigation_yes"] = application.has_pending_litigation
    data["pending_litigation_no"] = not application.has_pending_litigation
    data["unsatisfied_judgements_yes"] = application.has_unsatisfied_judgements
    data["unsatisfied_judgements_no"] = not application.has_unsatisfied_judgements
    data["been_bankrupt_yes"] = application.has_been_bankrupt
    data["been_bankrupt_no"] = not application.has_been_bankrupt
    data["refused_credit_yes"] = application.has_been_refused_credit
    data["refused_credit_no"] = not application.has_been_refused_credit
    data["ato_debt_yes"] = application.has_outstanding_ato_debt
    data["ato_debt_no"] = not application.has_outstanding_ato_debt
    data["tax_returns_yes"] = application.has_outstanding_tax_returns
    data["tax_returns_no"] = not application.has_outstanding_tax_returns
    data["payment_arrangements_yes"] = application.has_payment_arrangements
    data["payment_arrangements_no"] = not application.has_payment_arrangements
    
    # Property types for security properties
    security_properties = application.security_properties.all()
    for i, prop in enumerate(security_properties[:3]):
        prop_num = i + 1
        prefix = f"security{prop_num}"
        
        if prop.property_type:
            prop_type = prop.property_type.lower()
            data[f"{prefix}_residential"] = prop_type == "residential"
            data[f"{prefix}_commercial"] = prop_type == "commercial"
            data[f"{prefix}_rural"] = prop_type == "rural"
            data[f"{prefix}_industrial"] = prop_type == "industrial"
            data[f"{prefix}_vacant_land"] = prop_type == "land"
            data[f"{prefix}_other"] = prop_type == "other"
        
        # Property features
        if hasattr(prop, 'is_single_story'):
            data[f"{prefix}_single_story"] = prop.is_single_story
            data[f"{prefix}_double_story"] = not prop.is_single_story
        
        if hasattr(prop, 'has_garage'):
            data[f"{prefix}_garage"] = prop.has_garage
        if hasattr(prop, 'has_carport'):
            data[f"{prefix}_carport"] = prop.has_carport
        if hasattr(prop, 'has_off_street_parking'):
            data[f"{prefix}_off_street"] = prop.has_off_street_parking
        
        # Occupancy
        if prop.occupancy:
            data[f"{prefix}_owner_occupied"] = prop.occupancy == "owner_occupied"
            data[f"{prefix}_investment"] = prop.occupancy == "investment"
        
        # Valuation type (default to current value)
        data[f"{prefix}_valuation_current"] = True
        data[f"{prefix}_valuation_purchase"] = False
    
    # Loan purpose
    if application.loan_purpose:
        purpose = application.loan_purpose.lower()
        data["loan_purpose_purchase"] = purpose == "purchase"
        data["loan_purpose_refinance"] = purpose == "refinance"
        data["loan_purpose_construction"] = purpose == "construction"
        data["loan_purpose_equity_venture"] = purpose == "equity_release"
        data["loan_purpose_cash_out"] = "cash" in purpose
        data["loan_purpose_payout_debt"] = "debt" in purpose
        data["loan_purpose_other"] = purpose == "other"
    
    # Exit strategy
    if application.exit_strategy:
        exit_strat = application.exit_strategy.lower()
        data["exit_strategy_sale"] = exit_strat == "sale"
        data["exit_strategy_refinance"] = exit_strat == "refinance"
        data["exit_strategy_cash_flow"] = exit_strat == "income"
        data["exit_strategy_other"] = exit_strat == "other"
    
    # Other submissions (default to No)
    data["other_submissions_yes"] = False
    data["other_submissions_no"] = True
    
    return data


def format_date(date_obj) -> Optional[str]:
    """Format date object to DD/MM/YYYY string"""
    if date_obj:
        return date_obj.strftime("%d/%m/%Y")
    return None 