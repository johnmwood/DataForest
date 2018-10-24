from bs4 import BeautifulSoup
import pandas as pd 
import datetime 
import requests 
import re 


def request_table(offset): 
    url = f"https://finance.yahoo.com/sector/technology?offset={offset}&count=25"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    return soup.find_all("table")[1].find("tbody")

def create_stock(row):
    fields = ["symbol", "name", "price", "change", "change_percent",
              "volume", "three_month_avg_vol", "market_cap", "PE_ratio"]
    data = [x.text for x in row]

    return {key: value for key, value in zip(fields, data)}

def scrape_tables(): 
    table_range = [0, 100, 200, 300, 400, 446]
    all_stocks = [] 

    for offset in table_range: 
        table = request_table(offset) 

        for row in table: 
            stock = create_stock(row)
            all_stocks.append(stock)

    return all_stocks


all_stocks = scrape_tables() 
print(len(all_stocks))
print(all_stocks[0:5])

df = pd.DataFrame(all_stocks) 
df["date"] = datetime.datetime.today().strftime('%Y-%m-%d')
print(len(df))
# df.to_csv("stocks.csv")