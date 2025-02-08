# The code in this file calculates the 'score' the algorithm attributes to each company
# based on a normal distribution curve. This data is then used by the 'main.py' file
# to make the decision on whether to buy the company or not

from math import exp, sqrt, pi
from quant import *
from apikeys import *

def standardized_normal_dist(x : float, std : float, mean : float):
    """Returns the normal place of x in a normal distribution curve whose standard
       variation and expected value are passed as parameters."""
    peak_val = (1/sqrt(2 * pi * (std**2))) * exp(-((mean - mean)**2/(2 * std**2)))
    return ((1/sqrt(2 * pi * (std**2))) * exp(-((x - mean)**2/(2 * std**2))))/peak_val

def liabilities_to_equity_score(balance_sheet : dict):
    """Returns the score attributed to a company's liabilities to equity ratio."""
    lte = liabilities_to_equity(balance_sheet)
    return standardized_normal_dist(lte, 0.425, 1.0)

def liabilities_to_equity_score(balance_sheet : dict):
    """Returns the score attributed to a company's liabilities to equity ratio."""
    lte = liabilities_to_equity(balance_sheet)
    return standardized_normal_dist(lte, 0.425, 1.0)

test_tick = 'NVDA'
b_sheet = get_balance_sheet(test_tick, alphavantage_api_key)
print(liabilities_to_equity(b_sheet))
print(liabilities_to_equity_score(b_sheet))