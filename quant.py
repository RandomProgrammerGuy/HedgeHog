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

def get_income_statement(ticker : str, av_api_key : str):
    """Retrieves the financial statement of ticker. ticker has to be of type 
       string. Method requires an AlphaVantage API key as an argument."""
    
    
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={av_api_key}"
    url_req_response = requests.get(url)

    parsed_json = url_req_response.json()
    print_json(parsed_json)
