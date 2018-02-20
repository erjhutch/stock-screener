# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 10:28:29 2018

@author: EH

This script is based on a MATLAB script by Justin Riley that is available here:
https://www.mathworks.com/matlabcentral/fileexchange/46816-oshaughnessey-v5-m
"""

import requests
from bs4 import BeautifulSoup as bs

def get_page_data(soup):
    # returns table of ticker data given a beautiful soup object
    page_data = []
    counter = 0
    row_data = {}
    
    for td in soup.select(".screener-body-table-nw"):
        row_data[table_headers[counter]] = td.get_text()
        counter += 1
        if counter >= len(table_headers):
            counter = 0
            page_data.append(row_data)
            row_data = {}
    
    return page_data

def get_ev_ebitda(ticker):
    # returns ev/ebitda data from yahoo finance if found, otherwise nan
    YAHOO_URL = "https://finance.yahoo.com/quote/" #AAPL/key-statistics?p=AAPL
    url = YAHOO_URL + ticker + "/key-statistics?p=" + ticker
    r = requests.get(url)
    soup = bs(r.text, "lxml")
    
    # first find EV/EBITDA entry, then move to next td and return
    found = False
    for tr in soup.select("tr"):
        for td in soup.select("td"):
            if found:
                return float(td.get_text())
            elif td.get_text().startswith("Enterprise Value/EBITDA"):
                found = True
            else:
                continue
            
    # if not found return nan
    return float("nan")

# define some constants for the scraper
BASE_URL = "https://finviz.com/screener.ashx?v=152&f=cap_smallover&ft=4&"
START_URL = "c=0,1,2,3,4,7,10,11,13,45,65"

# get the first page
url = BASE_URL + START_URL
r = requests.get(url)
soup = bs(r.text, "lxml")

# find the last page number
pages = []
for pg in soup.select(".screener-pages"):
    pages.append(int(pg.get_text()))
#last_page = max(pages)
last_page = 2 # temp for testing

# get the table headers
table_headers = []
for th in soup.select(".table-top"):
        table_headers.append(th.get_text())
table_headers.insert(1, "Ticker") # add manually because ticker is table-top-s

# get all the stock data
stock_data = get_page_data(soup)

for pg in range(2,last_page+1):
    url = BASE_URL + "r=" + str(pg*20-19)
    r = requests.get(url)
    soup = bs(r.text, "lxml")
    stock_data += get_page_data(soup)    
    
    print("Current Progress: " + str(pg) + "/" + str(last_page))
    
# get EV/EBITDA data from Yahoo Finance
print(get_ev_ebitda("AAPL")) # just test once for now


