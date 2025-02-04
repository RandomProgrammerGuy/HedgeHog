# The code in this file does the qualitative analysis part of HedgeHog's stock 
# choices. This code uses the Google Gemeni API, which is free. To use it, go to the
# Google AI Studio website (https://aistudio.google.com) and claim an API key. Then,
# create a file named 'apikeys.py' and store your API key as a string in a variable
# called 'gemeni_api_key'. The file is in the .gitignore

import json
import google.generativeai as genai
from apikeys import gemeni_api_key

genai.configure(api_key=gemeni_api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("This is a test. Say Hello World in return.")

print(response.text)