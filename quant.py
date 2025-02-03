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
    
    if balance_sheet["annualReports"][0]["totalLiabilities"] == "None" or balance_sheet["annualReports"][0]["totalShareholderEquity"] == "None" or balance_sheet["annualReports"][0]["totalShareholderEquity"] == "0":
        return False
    
    return (int(balance_sheet["annualReports"][0]["totalLiabilities"]) / int(balance_sheet["annualReports"][0]["totalShareholderEquity"])) * 100

def liabilities_to_capital(balance_sheet : dict):
    """Calculates the Liabilities-to-Capital ratio of a company whose balance sheet is 
       passed as a dictionary-type argument. Returns False if it fails to calculate"""
    
    check_api_limit_reached(balance_sheet)
    
    if balance_sheet["annualReports"][0]["totalLiabilities"] == "None" or balance_sheet["annualReports"][0]["totalShareholderEquity"] == "None" or int(balance_sheet["annualReports"][0]["totalLiabilities"]) + int(balance_sheet["annualReports"][0]["totalShareholderEquity"]) == "0":
        return False
    
    return (int(balance_sheet["annualReports"][0]["totalLiabilities"]) / (int(balance_sheet["annualReports"][0]["totalLiabilities"]) + int(balance_sheet["annualReports"][0]["totalShareholderEquity"]))) * 100

def assets_to_equity(balance_sheet : dict):
    """Calculates the Total Assets-to-Equity ratio of a company whose balance sheet is 
       passed as a dictionary-type argument. Returns False if it fails to calculate"""
    
    check_api_limit_reached(balance_sheet)
    
    if balance_sheet["annualReports"][0]["totalAssets"] == "None" or balance_sheet["annualReports"][0]["totalShareholderEquity"] == "None" or balance_sheet["annualReports"][0]["totalShareholderEquity"] == "0":
        return False
    
    return (int(balance_sheet["annualReports"][0]["totalAssets"]) / int(balance_sheet["annualReports"][0]["totalShareholderEquity"])) * 100

def debt_to_ebitda(balance_sheet : dict, income_statement : dict):
    """Calculates the Total Debt-to-EBITDA ratio of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)
    check_api_limit_reached(income_statement)

    if balance_sheet["annualReports"][0]["totalLiabilities"] == "None" or income_statement["annualReports"][0]["ebitda"] == "None" or income_statement["annualReports"][0]["ebitda"] == "0":
            return False
    
    return (int(balance_sheet["annualReports"][0]["totalLiabilities"]) / int(income_statement["annualReports"][0]["ebitda"])) * 100

def quick_ratio(balance_sheet : dict):
    """Calculates the quick ratio of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)

    cash_plus_ce = balance_sheet["annualReports"][0]["cashAndCashEquivalentsAtCarryingValue"]
    ms = balance_sheet["annualReports"][0]["totalCurrentAssets"]
    nar = balance_sheet["annualReports"][0]["currentNetReceivables"]
    current_liabilities = balance_sheet["annualReports"][0]["totalCurrentLiabilities"]
    
    if cash_plus_ce == "None" or ms == "None" or nar == "None" or current_liabilities == "None" or current_liabilities == "0":
        return False
    
    return ((int(cash_plus_ce) + int(ms) + int(nar))/(int(current_liabilities)))*100


def current_ratio(balance_sheet : dict):
    """Calculates the current ratio of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)
    
    if balance_sheet["annualReports"][0]["totalCurrentAssets"] == "None" or balance_sheet["annualReports"][0]["totalCurrentLiabilities"] == "None" or balance_sheet["annualReports"][0]["totalCurrentLiabilities"] == "0":
        return False
    
    return (int(balance_sheet["annualReports"][0]["totalCurrentAssets"]) / int(balance_sheet["annualReports"][0]["totalCurrentLiabilities"]))*100

def ten_yr_operating_expenses_growth(income_statement : dict):
    """Calculates the 10yr op. expenses growth of a company whose income statement is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(income_statement)

    if income_statement["annualReports"][0]["operatingExpenses"] == "None" or income_statement["annualReports"][9]["operatingExpenses"] == "None" or income_statement["annualReports"][9]["operatingExpenses"] == "0":
        return False
    
    return ((int(income_statement["annualReports"][0]["operatingExpenses"]) - int(income_statement["annualReports"][9]["operatingExpenses"]))/(int(income_statement["annualReports"][9]["operatingExpenses"]))) * 100

def ten_yr_assets_growth(balance_sheet : dict):
    """Calculates the 10yr assets growth of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)

    if balance_sheet["annualReports"][0]["totalAssets"] == "None" or balance_sheet["annualReports"][9]["totalAssets"] == "None" or balance_sheet["annualReports"][9]["totalAssets"] == "0":
        return False
    
    return ((int(balance_sheet["annualReports"][0]["totalAssets"]) - int(balance_sheet["annualReports"][9]["totalAssets"]))/(int(balance_sheet["annualReports"][9]["totalAssets"]))) * 100

def ten_yr_liabilities_growth(balance_sheet : dict):
    """Calculates the 10yr liabilities growth of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)

    if balance_sheet["annualReports"][0]["totalLiabilities"] == "None" or balance_sheet["annualReports"][9]["totalLiabilities"] == "None" or balance_sheet["annualReports"][9]["totalLiabilities"] == "0":
        return False
    
    return ((int(balance_sheet["annualReports"][0]["totalLiabilities"]) - int(balance_sheet["annualReports"][9]["totalLiabilities"]))/(int(balance_sheet["annualReports"][9]["totalLiabilities"]))) * 100

def ten_yr_cash_flow_growth(cash_flow_report : dict):
    """Calculates the 10yr liabilities growth of a company whose cash flow report is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(cash_flow_report)

    if cash_flow_report["annualReports"][0]["operatingCashflow"] == "None" or cash_flow_report["annualReports"][9]["operatingCashflow"] == "None" or cash_flow_report["annualReports"][9]["operatingCashflow"] == "0":
        return False
    
    return ((int(cash_flow_report["annualReports"][0]["operatingCashflow"]) - int(cash_flow_report["annualReports"][9]["operatingCashflow"]))/(int(cash_flow_report["annualReports"][9]["operatingCashflow"]))) * 100

def ten_yr_share_count_growth(balance_sheet : dict):
    """Calculates the 10yr share count growth of a company whose balance sheet is 
    passed as a dictionary-type argument. Returns False if it fails to calculate"""

    check_api_limit_reached(balance_sheet)

    if balance_sheet["annualReports"][0]["commonStock"] == "None" or balance_sheet["annualReports"][9]["commonStock"] == "None" or balance_sheet["annualReports"][9]["commonStock"] == "0":
        return False
    
    return ((int(balance_sheet["annualReports"][0]["commonStock"]) - int(balance_sheet["annualReports"][9]["commonStock"]))/(int(balance_sheet["annualReports"][9]["commonStock"]))) * 100


b_sheet = get_balance_sheet("NVDA", alphavantage_api_key)
income_s = get_income_statement("NVDA", alphavantage_api_key)
cflow = get_cash_flow("NVDA", alphavantage_api_key)
earns = get_earnings("NVDA", alphavantage_api_key)

print("\nFUNDEMENTAL ANALYSIS                     NVDA")
print("---------------------------------------------")
print(f"       Liabilities-to-Equity Ratio : {liabilities_to_equity(b_sheet):.3f}%")
print(f"      Liabilities-to-Capital Ratio : {liabilities_to_capital(b_sheet):.3f}%")
print(f"            Assets-to-Equity Ratio : {assets_to_equity(b_sheet):.3f}%")
print(f"              Debt-to-EBITDA Ratio : {debt_to_ebitda(b_sheet, income_s):.3f}%")
print(f"                       Quick Ratio : {quick_ratio(b_sheet):.3f}%")
print(f"                     Current Ratio : {current_ratio(b_sheet):.3f}%")
print(f"Ten-Year Operating Expenses Growth : {ten_yr_operating_expenses_growth(income_s):.3f}%")
print(f"       Ten-Year Liabilities Growth : {ten_yr_liabilities_growth(b_sheet):.3f}%")
print(f"            Ten-Year Assets Growth : {ten_yr_assets_growth(b_sheet):.3f}%")
print(f"         Ten-Year Cash Flow Growth : {ten_yr_cash_flow_growth(cflow):.3f}%")
print(f"       Ten-Year Share Count Growth : {ten_yr_share_count_growth(b_sheet):.3f}%")