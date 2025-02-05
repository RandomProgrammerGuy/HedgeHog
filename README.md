# HedgeHog

Current Version: 0.0.0 INDEV-INCOMPLETE

# Important Notice

HedgeHog can make bad financial decisions. I advise all users to keep a track of the investments the program chooses and to research the stocks independently, being ready to intervene if the program makes a mistake. By using HedgeHog, the user agrees to assume all responsibility in case of financial loss or damages resulting directly or indirectly from the program's use.

# What is HedgeHog?
HedgeHog is an open-source, mid-to-long-term-focused stock portfolio manager. HedgeHog's investment model is based on fundamental analysis and market sentiment. For each stock, HedgeHog analyses the company's financial filings and calculates numerous ratios:

- Debt-to-Equity Ratio
- Debt-to-Capital Ratio
- Debt-to-EBITDA Ratio
- Assets-to-Equity Ratio
- Quick Ratio
- Current Ratio
- Ten-Year Operating Expenses Growth
- Ten-Year Liabilities Growth
- Ten-Year Assets Growth
- Ten-Year Cash Flow Growht
- Ten-Year Share Count Growth

It also conducts some market research on the company:

- Overall public sentiment toward the company
- Overall public sentiment toward the company's leadership
- Overall public sentiment toward the market sector
- Company's efforts in ESG, sustainability and responsible management
- Company's positioning amongst competitors (Coming in V1)

Based on the above-listed factors, HedgeHog makes one of three decisions:
- It may decide to recommend buying a company if it exhibits strong finances and is well-liked by the market
- It may decide to put a company on a watchlist if it isn't in great shape but has potential to grow in the near future
- It may decide against buying a company if it exhibits bad finances or the market is hostile against the company.

The amount of money it invests in each company it chooses depends on how much it "likes" the company based on the market and fundamental analysis results. It invests more money into companies that it believes to have the strongest chance of growth.

In v0 and v1, HedgeHog will only be analysing companies in the S&P 500. Starting from v2, it will analyse the entire US stock market. Non-US markets may come in the future although they are not guaranteed

# How does it do all of that?
HedgeHog is written entirely in Python and mainly uses two APIs to do its job:

- AlphaVantage API: Allows HedgeHog to access financial information about the company
- Google Gemeni API: Allows HedgeHog to analyse the market and the company using up-to-date online information 

# Current Developement State
HedgeHog is currently in early-stage developement and therefore non-functional. I am currently working on the base functions that retrieve financial and market information.

The first functional version, 0.0.1 Beta, is expected to release by the end of February 2025. I will be able to provide an anticipated release date for the first stable version (0.1.0) once 0.0.1 is released.

# Version Roadmap

### V0

HedgeHog V0 will be the first stable release of HedgeHog. At this stage it will be a simple stock picker that won't make any trades on the market by itself and it will only give recommendations on what to buy. It will not take into account the user's current portfolio.

Its stock list will be limited to the S&P 500. It is going to include a textual UI in the terminal.

### V1
HedgeHog V1 will be the first major update. The main new feature will be semi-active trading, meaning that while it will not be able to trade directly on the stock market itself, whenever it is run, it will ananlyse its portfolio and make changes if need be. HedgeHog V1 will be an actual trading algorithm instead of a stock picker. V1 may also bring along improvements to its analysis algorithms based on the results obtained in V0.

Its stock list will be limited to the S&P 500. It is going to include a textual UI in the terminal.

### V2
HedgeHog V2 will bring along fully-active trading, meaning that it will constantly monitor and change its portfolio as needed. However, it will still not be making active trades in the market on its own. V2 may also bring along improvements to its analysis algorithms based on the results obtained in V1.

Its stock list will be expanded to the entire US Stock Market. It is going to include a textual UI in the terminal.

### V3
HedgeHog V3 will be the first fully-autonomous version of HedgeHog. The fully active trading algorithm of V2 will now be used to make direct trades on the market when linked to a stock exchange account.

Its stock list will be expanded to the entire US Stock Market. It is going to include a textual UI in the terminal.

### V4 and Later

Coming soon!

# Who is behind HedgeHog?
HedgeHog is developed and maintained by Parsa Farjam, a CS-Math Double Degree student at Paris-Saclay University. 