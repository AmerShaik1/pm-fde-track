import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
city = "Atlanta"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

response = requests.get(url)
print(response.status_code)
print(response.json())