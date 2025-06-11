# The main decision-making process takes place in this file. The score calculation
# functions are imported from quant.py, and used here. As a reminder, you need to
# have an AlphaVantage API key stored in an apikeys.py file, in two variables called
# "alphavantage_api_key". This file is in the .gitignore, so as long as you don't modify
# it you can be assured that your API keys won't get published online.

# Also remember, the AlphaVantage API has a 25 request per day limit in the free version, 
# which can be  easily exceeded by HedgeHog. I have implemented a check function that 
# verifies every time the API is called if the limit is reached, and it will raise a 
# ConnectionRefusedError if it is.

import json
from quant import *
from scorecalc import *
from tickers import *
from apikeys import *
from time import sleep

# Startup splash screen
print('╻    ╻   ┏━━━━━   ━━━━━┓   ┏━━━━━   ┏━━━━━      ╻    ╻   ┏━━━━┓   ┏━━━━━')
print('┃    ┃   ┃         ┃   ┃   ┃        ┃           ┃    ┃   ┃    ┃   ┃     ')
print('┣━━━━┫   ┣━━━━     ┃   ┃   ┃  ━━┓   ┣━━━━━      ┣━━━━┫   ┃    ┃   ┃  ━━┓')
print('┃    ┃   ┃         ┃   ┃   ┃    ┃   ┃           ┃    ┃   ┃    ┃   ┃    ┃')
print('╹    ╹   ┗━━━━━   ━━━━━┛   ┗━━━━┛   ┗━━━━━      ╹    ╹   ┗━━━━┛   ┗━━━━┛')

# Get total investment budget from user
print('')

print('Enter your total investment budget: ', end='')

total_budget = float(input())

print('')

test_set = ['AMZN'] # Will be replaced by variable 'sp500' from 'tickers' module in full version

# Will include the companies the algorithm has decided to buy
cart = {}

# Main decision-making loop. If you get errors in this part it is probably due to the API
for company in test_set:
    print(f'■ Currently Analysing: {company}\n')

    scores = []

    company_income_statement = get_income_statement(company, alphavantage_api_key)
    company_balance_sheet = get_balance_sheet(company, alphavantage_api_key)

    scores.append(liabilities_to_equity_score(company_balance_sheet))
    print(f'Debt-to-Equity Ratio: \n{liabilities_to_equity(company_balance_sheet)}')
    print(f'Debt-to-Equity Atrributed Score: \n{scores[-1]}')
    print('━━━━━━━━━━')

    # sleep(0.2)

    scores.append(liabilities_to_capital_score(company_balance_sheet))
    print(f'Debt-to-Capital Ratio: \n{liabilities_to_capital(company_balance_sheet)}')
    print(f'Debt-to-Capital Atrributed Score: \n{scores[-1]}')
    print('━━━━━━━━━━')

    # sleep(0.2)

    scores.append(float(assets_to_equity_score(company_balance_sheet)))
    print(f'Assets-to-Equity Ratio: \n{assets_to_equity(company_balance_sheet)}')
    print(f'Assets-to-Equity Atrributed Score: \n{scores[-1]}')
    print('━━━━━━━━━━')

    # sleep(0.2)

    scores.append(float(debt_to_ebitda_score(company_balance_sheet, company_income_statement)))
    print(f'Debt-to-EBITDA Ratio: \n{debt_to_ebitda(company_balance_sheet, company_income_statement)}')
    print(f'Debt-to-EBITDA Atrributed Score: \n{scores[-1]}')
    print('━━━━━━━━━━')

    # sleep(0.2)

    scores.append(float(quick_ratio_score(company_balance_sheet)))
    print(f'Quick Ratio: \n{quick_ratio(company_balance_sheet)}')
    print(f'Quick Ratio Atrributed Score: \n{scores[-1]}')
    print('━━━━━━━━━━')

    # sleep(0.2)

    scores.append(float(current_ratio_score(company_balance_sheet)))
    print(f'Current Ratio: \n{current_ratio(company_balance_sheet)}')
    print(f'Current Ratio Atrributed Score: \n{scores[-1]}')
    print('━━━━━━━━━━')

    # sleep(0.2)

    status = ten_yr_operating_expenses_growth(company_income_statement)

    if status != False:
        scores.append(float(ten_yr_opex_growth_score(company_income_statement)))
        print(f'10-Year Operating Expenses Growth: \n{status}')
        print(f'10-Year Operating Expenses Growth Atrributed Score: \n{scores[-1]}')
        print('━━━━━━━━━━')

    # sleep(0.2)

    status = ten_yr_assets_growth(company_balance_sheet)
    if status != False:
        scores.append(float(ten_yr_assets_growth_score(company_balance_sheet)))
        print(f'10-Year Assets Growth: \n{status}')
        print(f'10-Year Assets Growth Atrributed Score: \n{scores[-1]}')
        print('━━━━━━━━━━')

    # sleep(0.2)

    status = one_yr_liabilities_growth(company_balance_sheet)
    if status != False:
        scores.append(float(one_yr_liabilities_growth_score(company_balance_sheet)))
        print(f'1-Year Liabilities Growth: \n{status}')
        print(f'1-Year Liabilities Growth Atrributed Score: \n{scores[-1]}')
        print('━━━━━━━━━━')

    # sleep(0.2)

    status = two_yr_liabilities_growth(company_balance_sheet)
    if status != False:
        scores.append(float(two_yr_liabilities_growth_score(company_balance_sheet)))
        print(f'2-Year Liabilities Growth: \n{status}')
        print(f'2-Year Liabilities Growth Atrributed Score: \n{scores[-1]}')
        print('━━━━━━━━━━')

    # sleep(0.2)

    status = five_yr_liabilities_growth(company_balance_sheet)
    if status != False:
        scores.append(float(five_yr_liabilities_growth_score(company_balance_sheet)))
        print(f'5-Year Liabilities Growth: \n{status}')
        print(f'5-Year Liabilities Growth Atrributed Score: \n{scores[-1]}')
        print('━━━━━━━━━━')

    # sleep(0.2)

    status = ten_yr_liabilities_growth(company_balance_sheet)
    if status != False:
        scores.append(float(ten_yr_liabilities_growth_score(company_balance_sheet)))
        print(f'10-Year Liabilities Growth: \n{status}')
        print(f'10-Year Liabilities Growth Atrributed Score: \n{scores[-1]}')
        print('━━━━━━━━━━')

    #sleep(0.2)

    status = ten_yr_share_count_growth(company_balance_sheet)

    if status != False:
        scores.append(float(ten_yr_share_count_growth_score(company_balance_sheet)))
        print(f'10-Year Share Count Growth: \n{status}')
        print(f'10-Year Share Count Growth Atrributed Score: \n{scores[-1]}')
        print('━━━━━━━━━━')

# Sorts the cart by score values
sorted_cart = {key: value for key, 
               value in sorted(cart.items(), 
                               key=lambda item: item[1])}

sorted_cart_selection = dict(list(sorted_cart.items())[len(sorted_cart) // 2:])

# Writes to portfolio file
portfolio_file = open('portfolio.txt', 'w')

print('WRITING ANALYSIS RESULTS TO "portfolio.txt"')
for pick in sorted_cart_selection:
    line = f"Buy {(sorted_cart_selection[pick]/sum(list(sorted_cart_selection.values()))) * (total_budget):.2f}$ of {pick} shares\n"
    portfolio_file.write(line)

print('File write completed. Exiting program...')

portfolio_file.close()
