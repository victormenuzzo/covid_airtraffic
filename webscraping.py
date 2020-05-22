import pandas as pd
from bs4 import BeautifulSoup
import requests
import smtplib
import time

df = pd.read_csv("flightlist_20200101_20200131.csv") 

i=1
df['service_type'] = 0

for teste in df[['callsign']].values:
    URL = "https://planefinder.net/data/flight/"+str(teste[0])+"?#"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    headers = {"user-agent": user_agent}
    req = requests.get(URL, headers=headers)
    # get price
    soup = BeautifulSoup(req.text, "html.parser")
    span = soup.find_all("span", "value") # <span id="priceblock_ourprice">...</span>
    service_type = span[6].text 
    df[df.callsign == teste[0]] = service_type
    print(str(i) +" " + str(teste[0]) +" "+ str(service_type))
    i=i+1
df.to_csv('flights_202001.csv')
