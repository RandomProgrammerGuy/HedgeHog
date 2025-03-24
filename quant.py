# The code in this file does the quantitative analysis part of HedgeHog's stock 
# choices. This code uses the AlphaVantage API, which is free. To use it, go to the
# AlphaVantage website (https://www.alphavantage.co) and claim an API key. Once done,
# create a file named 'apikeys.py' and store your API key as a string in a variable
# called 'alphavantage_api_key'. The file is in the .gitignore

import json
import requests
from apikeys import alphavantage_api_key

def print_json(data : dict):
    """Prints JSON data in a more presentable way. Mainly used for Debugging."""
    print(json.dumps(data, indent=4))

def alphavantage_api_request(ticker : str, function : str, av_api_key : str):
    """Auxiliary function that allows for easier AlphaVantage API calls"""
    req_rep =  requests.get(f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={av_api_key}")
    check_api_limit_reached(req_rep)
    return req_rep

def check_api_limit_reached(param : dict) :
    """Checks if the AlphaVantage API call limit is reached when the API is called"""
    if param == {'Information': 'Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits.'} :
        raise ConnectionRefusedError("ALPHA VANTAGE API REQUEST LIMIT REACHED. TRY AGAIN LATER, SUBSCRIBE TO PREMIUM OR CHANGE THE API KEY IN apikeys.py")
    

def get_income_statement(ticker : str, av_api_key : str):
    """Retrieves the financial statement of a ticker. ticker has to be of type 
       string. Function requires an AlphaVantage API key as an argument."""
    
    api_req_response = alphavantage_api_request(ticker, 'INCOME_STATEMENT', av_api_key)
    check_api_limit_reached(api_req_response)
    parsed_json = api_req_response.json()
    return parsed_json

def get_balance_sheet(ticker : str, av_api_key : str):
    """Retrieves the balance sheet of a ticker. ticker has to be of type string.
       Function requires an AlphaVantage API key as an argument"""
    
    api_req_response = alphavantage_api_request(ticker, 'BALANCE_SHEET', av_api_key)
    check_api_limit_reached(api_req_response)
    parsed_json = api_req_response.json()
    return parsed_json

def get_cash_flow(ticker : str, av_api_key : str):
    """Retrieves the cash flow of a ticker. ticker has to be of type string.
    Function requires an AlphaVantage API key as an argument"""
    
    api_req_response = alphavantage_api_request(ticker, 'CASH_FLOW', av_api_key)
    check_api_limit_reached(api_req_response)
    parsed_json = api_req_response.json()
    return parsed_json


def get_earnings(ticker : str, av_api_key : str):
    """Retrieves the cash earnings of a ticker. ticker has to be of type string.
    Function requires an AlphaVantage API key as an argument"""
    
    api_req_response = alphavantage_api_request(ticker, 'EARNINGS', av_api_key)
    check_api_limit_reached(api_req_response)
    parsed_json = api_req_response.json()
    return parsed_json

def liabilities_to_equity(balance_sheet : dict):
    """Calculates the Libailities-to-Equity ratio of a company whose balance sheet is 
       passed as a dictionary-type argument. Returns False if it fails to calculate"""
    
    check_api_limit_reached(balance_sheet)
    
    if balance_sheet["annualReports"][1]["totalLiabilities"] == "None" or balance_sheet["annualReports"][1]["totalShareholderEquity"] == "None" or balance_sheet["annualReports"][1]["totalShareholderEquity"] == "0":
        return False
    
    return (int(balance_sheet["annualReports"][1]["totalLiabilities"]) / int(balance_sheet["annualReports"][1]["totalShareholderEquity"]))

def liabilities_to_capital(balance_sheet : dict):
    """Calculates the Liabilities-to-Capital ratio of a company whose balance sheet is 
       passed as a dictionary-type argument. Returns False if it fails to calculate"""
    
    check_api_limit_reached(balance_sheet)
    
    if balance_sheet["annualReports"][1]["totalLiabilities"] == "None" or balance_sheet["annualReports"][1]["totalShareholderEquity"] == "None" or int(balance_sheet["annualReports"][1]["totalLiabilities"]) + int(balance_sheet["annualReports"][1]["totalShareholderEquity"]) == "0":
        return False
    
    return (int(balance_sheet["annualReports"][1]["totalLiabilities"]) / (int(balance_sheet["annualReports"][1]["totalLiabilities"]) + int(balance_sheet["annualReports"][1]["totalShareholderEquity"])))

def assets_to_equity(balance_sheet : dict):
    """Calculates the Total Assets-to-Equity ratio of a company whose balance sheet is 
       passed as a dictionary-type argument. Returns False if it fails to calculate"""
    
    check_api_limit_reached(balance_sheet)
    
    if balance_sheet["annualReports"][1]["totalAssets"] == "None" or balance_sheet["annualReports"][1]["totalShareholderEquity"] == "None" or balance_sheet["annualReports"][1]["totalShareholderEquity"] == "0":
        return False
    
    return (int(balance_sheet["annualReports"][1]["totalAssets"]) / int(balance_sheet["annualReports"][1]["totalShareholderEquity"]))

def debt_to_ebitda(balance_sheet : dict, income_statement : dict):
    """Calculates the Total Debt-to-EBITDA ratio of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)
    check_api_limit_reached(income_statement)

    if balance_sheet["annualReports"][1]["totalLiabilities"] == "None" or income_statement["annualReports"][1]["ebitda"] == "None" or income_statement["annualReports"][1]["ebitda"] == "0":
            return False
    
    return (int(balance_sheet["annualReports"][1]["totalLiabilities"]) / int(income_statement["annualReports"][1]["ebitda"]))

def quick_ratio(balance_sheet : dict):
    """Calculates the quick ratio of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)

    cash_plus_ce = balance_sheet["annualReports"][1]["cashAndCashEquivalentsAtCarryingValue"]
    ms = balance_sheet["annualReports"][1]["totalCurrentAssets"]
    nar = balance_sheet["annualReports"][1]["currentNetReceivables"]
    current_liabilities = balance_sheet["annualReports"][1]["totalCurrentLiabilities"]
    
    if cash_plus_ce == "None" or ms == "None" or nar == "None" or current_liabilities == "None" or current_liabilities == "0":
        return False
    
    return ((int(cash_plus_ce) + int(ms) + int(nar))/(int(current_liabilities)))


def current_ratio(balance_sheet : dict):
    """Calculates the current ratio of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)
    
    if balance_sheet["annualReports"][1]["totalCurrentAssets"] == "None" or balance_sheet["annualReports"][1]["totalCurrentLiabilities"] == "None" or balance_sheet["annualReports"][1]["totalCurrentLiabilities"] == "0":
        return False
    
    return (int(balance_sheet["annualReports"][1]["totalCurrentAssets"]) / int(balance_sheet["annualReports"][1]["totalCurrentLiabilities"]))

def ten_yr_operating_expenses_growth(income_statement : dict):
    """Calculates the 10yr op. expenses growth of a company whose income statement is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(income_statement)

    if income_statement["annualReports"][1]["operatingExpenses"] == "None" or income_statement["annualReports"][10]["operatingExpenses"] == "None" or income_statement["annualReports"][10]["operatingExpenses"] == "0":
        return False
    
    return ((int(income_statement["annualReports"][1]["operatingExpenses"]) - int(income_statement["annualReports"][10]["operatingExpenses"]))/(int(income_statement["annualReports"][10]["operatingExpenses"]))) * 100

def ten_yr_assets_growth(balance_sheet : dict):
    """Calculates the 10yr assets growth of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)
    
    if len(balance_sheet["annualReports"]) < 11 :
        return False
    
    if balance_sheet["annualReports"][1]["totalAssets"] == "None" or balance_sheet["annualReports"][10]["totalAssets"] == "None" or balance_sheet["annualReports"][10]["totalAssets"] == "0" :
        return False
    
    return ((int(balance_sheet["annualReports"][1]["totalAssets"]) - int(balance_sheet["annualReports"][10]["totalAssets"]))/(int(balance_sheet["annualReports"][10]["totalAssets"]))) * 100

def ten_yr_liabilities_growth(balance_sheet : dict):
    """Calculates the 10yr liabilities growth of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)

    if len(balance_sheet["annualReports"]) < 11 :
        return False

    if balance_sheet["annualReports"][1]["totalLiabilities"] == "None" or balance_sheet["annualReports"][10]["totalLiabilities"] == "None" or balance_sheet["annualReports"][10]["totalLiabilities"] == "0":
        return False
    
    return ((int(balance_sheet["annualReports"][1]["totalLiabilities"]) - int(balance_sheet["annualReports"][10]["totalLiabilities"]))/(int(balance_sheet["annualReports"][10]["totalLiabilities"]))) * 100

def ten_yr_cash_flow_growth(cash_flow_report : dict):
    """Calculates the 10yr liabilities growth of a company whose cash flow report is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(cash_flow_report)

    if len(cash_flow_report["annualReports"]) < 11 :
        return False

    if cash_flow_report["annualReports"][1]["operatingCashflow"] == "None" or cash_flow_report["annualReports"][10]["operatingCashflow"] == "None" or cash_flow_report["annualReports"][10]["operatingCashflow"] == "0":
        return False
    
    return ((int(cash_flow_report["annualReports"][1]["operatingCashflow"]) - int(cash_flow_report["annualReports"][10]["operatingCashflow"]))/(int(cash_flow_report["annualReports"][10]["operatingCashflow"]))) * 100

def ten_yr_share_count_growth(balance_sheet : dict):
    """Calculates the 10yr share count growth of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)

    if len(balance_sheet["annualReports"]) < 11 :
        return False

    if balance_sheet["annualReports"][1]["commonStock"] == "None" or balance_sheet["annualReports"][10]["commonStock"] == "None" or balance_sheet["annualReports"][10]["commonStock"] == "0":
        return False
    
    return ((int(balance_sheet["annualReports"][1]["commonStock"]) - int(balance_sheet["annualReports"][10]["commonStock"]))/(int(balance_sheet["annualReports"][10]["commonStock"]))) * 100
