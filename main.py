# The main decision-making process takes place in this file. The score calculation
# functions are imported from quant.py and qualit.py, and used here. As a reminder,
# you need to have an AlphaVantage API key and a Google Gemeni API key stored in an
# apikeys.py file, in two variables called "alphavantage_api_key" and "gemeni_api_key".
# This file is in the .gitignore, so as long as you don't modify it you can be assured
# that your API keys won't get published online. Also remember, the AlphaVantage API
# has a 25 request per day limit in the free version, which will be pretty easily
# exceeded by HedgeHog. I have implemented a check function that verifies every time
# the API is called if the limit is reached, and it will raise a ConnectionRefusedError
# if it is.

import json
from qualit import *
from quant import *
from scorecalc import *
from tickers import *
from apikeys import *
from time import sleep

print('■   ■   ■■■■■   ■■■■■   ■■■■■   ■■■■■      ■   ■   ■■■■■   ■■■■■')
print('■   ■   ■        ■  ■   ■       ■          ■   ■   ■   ■   ■    ')
print('■■■■■   ■■■■■    ■  ■   ■  ■■   ■■■■■      ■■■■■   ■   ■   ■  ■■')
print('■   ■   ■        ■  ■   ■   ■   ■          ■   ■   ■   ■   ■   ■')
print('■   ■   ■■■■■   ■■■■■   ■■■■■   ■■■■■      ■   ■   ■■■■■   ■■■■■')

test_set = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'META']

for company in test_set:
    print(f'■ Currently Analysing: {company}')

    scores = []

    company_income_statement = get_income_statement(company, alphavantage_api_key)
    company_balance_sheet = get_balance_sheet(company, alphavantage_api_key)

    scores.append(liabilities_to_equity_score(company_balance_sheet))
    print(f'Debt-to-Equity Ratio: {liabilities_to_equity(company_balance_sheet)}')
    print(f'Debt-to-Equity Atrributed Score: {scores[-1]}')

    sleep(0.1)

    scores.append(liabilities_to_capital_score(company_balance_sheet))
    print(f'Debt-to-Capital Ratio: {liabilities_to_capital(company_balance_sheet)}')
    print(f'Debt-to-Capital Atrributed Score: {scores[-1]}')

    sleep(0.1)

    scores.append(float(assets_to_equity_score(company_balance_sheet)))
    print(f'Assets-to-Equity Ratio: {assets_to_equity(company_balance_sheet)}')
    print(f'Assets-to-Equity Atrributed Score: {scores[-1]}')

    sleep(0.1)

    scores.append(float(debt_to_ebitda_score(company_balance_sheet, company_income_statement)))
    print(f'Debt-to-EBITDA Ratio: {debt_to_ebitda(company_balance_sheet, company_income_statement)}')
    print(f'Debt-to-EBITDA Atrributed Score: {scores[-1]}')

    sleep(0.1)

    scores.append(float(quick_ratio_score(company_balance_sheet)))
    print(f'Quick Ratio: {quick_ratio(company_balance_sheet)}')
    print(f'Quick Ratio Atrributed Score: {scores[-1]}')

    sleep(0.1)

    scores.append(float(current_ratio_score(company_balance_sheet)))
    print(f'Current Ratio: {current_ratio(company_balance_sheet)}')
    print(f'Current Ratio Atrributed Score: {scores[-1]}')

    sleep(0.1)

    scores.append(float(ten_yr_opex_growth_score(company_income_statement)))
    print(f'10-Year Operating Expenses Growth: {ten_yr_operating_expenses_growth(company_income_statement)}')
    print(f'10-Year Operating Expenses Growth Atrributed Score: {scores[-1]}')

    sleep(0.1)

    scores.append(float(ten_yr_assets_growth_score(company_balance_sheet)))
    print(f'10-Year Assets Growth: {ten_yr_assets_growth(company_balance_sheet)}')
    print(f'10-Year Assets Growth Atrributed Score: {scores[-1]}')

    sleep(0.1)

    scores.append(float(ten_yr_liabilities_growth_score(company_balance_sheet)))
    print(f'10-Year Liabilities Growth: {ten_yr_liabilities_growth(company_balance_sheet)}')
    print(f'10-Year Liabilities Growth Atrributed Score: {scores[-1]}')

    sleep(0.1)

    scores.append(float(ten_yr_share_count_growth_score(company_balance_sheet)))
    print(f'10-Year Share Count Growth: {ten_yr_share_count_growth(company_balance_sheet)}')
    print(f'10-Year Share Count Growth Atrributed Score: {scores[-1]}')

    sleep(0.1)

    scores.append(float(analyse_public_sentiment_company(company)))
    print(f'Public Sentiment Towards the Company {scores[-1]}')

    sleep(0.1)

    scores.append(float(analyse_public_sentiment_leadership(company)))
    print(f'Public Sentiment Towards the Company\'s Leadership {scores[-1]}')

    sleep(0.1)

    scores.append(float(analyse_public_sentiment_sector(company)))
    print(f'Public Sentiment Towards the Company\'s Industry Sector {scores[-1]}')

    sleep(0.1)

    scores.append(float(analyse_esg_and_sustainability(company)))
    print(f'The Company\'s ESG and Sustainability Efforts {scores[-1]}')

    sleep(0.1)

    scores_avg = sum(scores) / len(scores)
    print(f'Company\'s Average Score {scores_avg}')

    sleep(0.1)

    if scores_avg > 0.50:
        print('DECISION: BUY')
    elif 0.25 < scores_avg <= 50:
        print('DECISION: WAITLIST')
    else:
        print('DECISION: AVOID')

    print(' ')
    sleep(2)