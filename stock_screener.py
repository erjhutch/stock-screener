# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 10:28:29 2018

@author: EH

This script is based on a MATLAB script by Justin Riley, available here:
https://www.mathworks.com/matlabcentral/fileexchange/46816-oshaughnessey-v5-m

"""

import requests
from bs4 import BeautifulSoup as bs

# get html
r = requests.get('https://finviz.com/screener.ashx?v=152&f=cap_smallover&ft=4&c=0,1,2,3,4,7,10,11,13,45,65')
soup = bs(r.text, "lxml")

# get table headers
table_headers = []
for th in soup.select(".table-top"):
        table_headers.append(th.get_text())
table_headers.insert(1, "Ticker") # Doesn't find ticker column, because selected column is table-top-s

# get row data
table_row_data = []
counter = 0
row_data = {}

for tr in soup.select(".screener-body-table-nw"):
    row_data[table_headers[counter]] = tr.get_text()
    counter += 1
    if counter >= len(table_headers):
        counter = 0
        table_row_data.append(row_data)
        row_data = {}
        
# some examples
print(table_row_data[9]) # Print row of data
print(table_row_data[9]["Ticker"]) # Print ticker at index 9
print(table_row_data[9]["Price"]) # Print AAPL price

