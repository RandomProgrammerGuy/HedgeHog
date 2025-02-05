# The code in this file does the qualitative analysis part of HedgeHog's stock 
# choices. This code uses the Google Gemeni API, which is free. To use it, go to the
# Google AI Studio website (https://aistudio.google.com) and claim an API key. Then,
# create a file named 'apikeys.py' and store your API key as a string in a variable
# called 'gemeni_api_key'. The file is in the .gitignore

import json
import google.generativeai as genai
from apikeys import gemeni_api_key

genai.configure(api_key=gemeni_api_key)

gemeni = genai.GenerativeModel("gemini-1.5-flash")

def analyse_public_sentiment_company(ticker : str):
    response = gemeni.generate_content(f"Analyse the general sentiment towards the brand image of the company whose ticker is {ticker}. YOUR RESPONSE SHOULD ONLY INCLUDE A NUMBER BETWEEN 0 (= THE COMPANY IS VERY HATED) AND 1 (= THE COMPANY IS VERY LOVED). The score should follow a normal distribution curve. BE BRUTALLY HONEST AND OBJECTIVE. If the company has encountered large scandals or lawsuits in the past year this score should be low. Recent news should have a noticeable impact on this score.")
    return response.text.strip()

def analyse_public_sentiment_leadership(ticker : str):
    response = gemeni.generate_content(f"Analyse the general sentiment towards the leadership (MOST especially the CEO) of the company whose ticker is {ticker}. YOUR RESPONSE SHOULD ONLY INCLUDE A NUMBER BETWEEN 0 (= THE LEADERSHIP IS VERY HATED) AND 1 (= THE LEADERSHIP IS VERY LOVED). The score should follow a normal distribution curve. BE BRUTALLY HONEST AND OBJECTIVE. If the CEO or other high management has been involved in many scandals this score should be low.")
    return response.text.strip()

def analyse_public_sentiment_sector(ticker : str):
    response = gemeni.generate_content(f"Analyse the general sentiment towards the industry sector of the company whose ticker is {ticker}. YOUR RESPONSE SHOULD ONLY INCLUDE A NUMBER BETWEEN 0 (= THE SECTOR IS VERY HATED) AND 1 (= THE SECTOR IS VERY LOVED). The score should follow a normal distribution curve. BE BRUTALLY HONEST AND OBJECTIVE. Analyse the sector independently from the company itself. If the sector is an enviornmentally-damaging one (like oil or natural gas), it should get a lower score.")
    return response.text.strip()

def analyse_esg_and_sustainability(ticker : str):
    response = gemeni.generate_content(f"How enviornmentally and morally responsible is the company whose ticker is {ticker}? Are they good with ESG? YOUR RESPONSE SHOULD ONLY INCLUDE A NUMBER BETWEEN 0 (= THE COMPANY IS VERY IRRESPONSIBLE/IMMORAL) AND 1 (= THE COMPANY IS VERY RESPONSIBLE). The score should follow a normal distribution curve. BE BRUTALLY HONEST AND OBJECTIVE. If a company's operation sector is an enviornmentally-damaging one (like oil or natural gas), it should get a lower score.")
    return response.text.strip()

tick = "TSLA"
print(f"\nCOMPANY TICKER: {tick}")
print( "___________________________________________")
print(f"Public sentiment towards company    | {analyse_public_sentiment_company(tick)} |")
print(f"Public sentiment towards leadership | {analyse_public_sentiment_leadership(tick)} |")
print(f"Public sentiment towards sector     | {analyse_public_sentiment_sector(tick)} |")
print(f"ESG and sustainability score        | {analyse_esg_and_sustainability(tick)} |")
print( "___________________________________________\n")

tick = "MSFT"
print(f"\nCOMPANY TICKER: {tick}")
print( "___________________________________________")
print(f"Public sentiment towards company    | {analyse_public_sentiment_company(tick)} |")
print(f"Public sentiment towards leadership | {analyse_public_sentiment_leadership(tick)} |")
print(f"Public sentiment towards sector     | {analyse_public_sentiment_sector(tick)} |")
print(f"ESG and sustainability score        | {analyse_esg_and_sustainability(tick)} |")
print( "___________________________________________\n")

tick = "XOM"
print(f"\nCOMPANY TICKER: {tick}")
print( "___________________________________________")
print(f"Public sentiment towards company    | {analyse_public_sentiment_company(tick)} |")
print(f"Public sentiment towards leadership | {analyse_public_sentiment_leadership(tick)} |")
print(f"Public sentiment towards sector     | {analyse_public_sentiment_sector(tick)} |")
print(f"ESG and sustainability score        | {analyse_esg_and_sustainability(tick)} |")
print( "___________________________________________\n")