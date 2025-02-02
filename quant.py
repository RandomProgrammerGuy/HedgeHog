# The code in this file does the quantitative analysis part of the HedgeHog's stock 
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
    return requests.get(f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={av_api_key}")

def get_income_statement(ticker : str, av_api_key : str):
    """Retrieves the financial statement of a ticker. ticker has to be of type 
       string. Function requires an AlphaVantage API key as an argument."""
    
    api_req_response = alphavantage_api_request(ticker, 'INCOME_STATEMENT', av_api_key)
    parsed_json = api_req_response.json()
    return parsed_json

def get_balance_sheet(ticker : str, av_api_key : str):
    """Retrieves the balance sheet of a ticker. ticker has to be of type string.
       Function requires an AlphaVantage API key as an argument"""
    
    api_req_response = alphavantage_api_request(ticker, 'BALANCE_SHEET', av_api_key)
    parsed_json = api_req_response.json()
    return parsed_json

def get_cash_flow(ticker : str, av_api_key : str):
    """Retrieves the cash flow of a ticker. ticker has to be of type string.
    Function requires an AlphaVantage API key as an argument"""
    
    api_req_response = alphavantage_api_request(ticker, 'CASH_FLOW', av_api_key)
    parsed_json = api_req_response.json()
    return parsed_json


def get_earnings(ticker : str, av_api_key : str):
    """Retrieves the cash earnings of a ticker. ticker has to be of type string.
    Function requires an AlphaVantage API key as an argument"""
    
    api_req_response = alphavantage_api_request(ticker, 'EARNINGS', av_api_key)
    parsed_json = api_req_response.json()
    return parsed_json

def liabilities_to_equity(balance_sheet : dict):
    """Calculates the Libailities-to-Equity ratio of a company whose balance sheet is 
       passed as a dictionary-type argument. Returns -1 if it fails to calculate"""
    
    if balance_sheet["annualReports"][0]["totalLiabilities"] == "None" or balance_sheet["annualReports"][0]["totalShareholderEquity"] == "None" or balance_sheet["annualReports"][0]["totalShareholderEquity"] == "0":
        return -1
    
    return int(balance_sheet["annualReports"][0]["totalLiabilities"]) / int(balance_sheet["annualReports"][0]["totalShareholderEquity"])

def liabilities_to_capital(balance_sheet : dict):
    """Calculates the Liabilities-to-Capital ratio of a company whose balance sheet is 
       passed as a dictionary-type argument. Returns -1 if it fails to calculate"""
    
    if balance_sheet["annualReports"][0]["totalLiabilities"] == "None" or balance_sheet["annualReports"][0]["totalShareholderEquity"] == "None" or int(balance_sheet["annualReports"][0]["totalLiabilities"]) + int(balance_sheet["annualReports"][0]["totalShareholderEquity"]) == "0":
        return -1
    
    return int(balance_sheet["annualReports"][0]["totalLiabilities"]) / (int(balance_sheet["annualReports"][0]["totalLiabilities"]) + int(balance_sheet["annualReports"][0]["totalShareholderEquity"]))

def assets_to_equity(balance_sheet : dict):
    """Calculates the Total Assets-to-Equity ratio of a company whose balance sheet is 
       passed as a dictionary-type argument. Returns -1 if it fails to calculate"""
    
    if balance_sheet["annualReports"][0]["totalAssets"] == "None" or balance_sheet["annualReports"][0]["totalShareholderEquity"] == "None" or balance_sheet["annualReports"][0]["totalShareholderEquity"] == "0":
        return -1
    
    return int(balance_sheet["annualReports"][0]["totalAssets"]) / int(balance_sheet["annualReports"][0]["totalShareholderEquity"])

def debt_to_ebitda(balance_sheet : dict, income_statement : dict):
    """Calculates the Total Debt-to-EBITDA ratio of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns -1 if it fails to calculate"""

    if balance_sheet["annualReports"][0]["totalLiabilities"] == "None" or income_statement["annualReports"][0]["ebitda"] == "None" or income_statement["annualReports"][0]["ebitda"] == "0":
            return -1
    
    return int(balance_sheet["annualReports"][0]["totalLiabilities"]) / int(income_statement["annualReports"][0]["ebitda"])

def quick_ratio(balance_sheet : dict):
    """Calculates the quick ratio of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns -1 if it fails to calculate"""
    cash_plus_ce = balance_sheet["annualReports"][0]["cashAndCashEquivalentsAtCarryingValue"]
    ms = balance_sheet["annualReports"][0]["totalCurrentAssets"]
    nar = balance_sheet["annualReports"][0]["currentNetReceivables"]
    current_liabilities = balance_sheet["annualReports"][0]["totalCurrentLiabilities"]
    
    if cash_plus_ce == "None" or ms == "None" or nar == "None" or current_liabilities == "None" or current_liabilities == "0":
        return -1
    
    return (int(cash_plus_ce) + int(ms) + int(nar))/(int(current_liabilities))


def current_ratio(balance_sheet : dict):
    """Calculates the current ratio of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns -1 if it fails to calculate"""
    if balance_sheet["annualReports"][0]["totalCurrentAssets"] == "None" or balance_sheet["annualReports"][0]["totalCurrentLiabilities"] == "None" or balance_sheet["annualReports"][0]["totalCurrentLiabilities"] == "0":
        return -1
    
    return int(balance_sheet["annualReports"][0]["totalCurrentAssets"]) / int(balance_sheet["annualReports"][0]["totalCurrentLiabilities"])

def ten_year_operating_expenses_growth(income_statement : dict):
    """Calculates the 10yr op. expenses growth of a company whose income statement is 
    passed as a dictionary-type argument. Returns -1 if it fails to calculate"""

