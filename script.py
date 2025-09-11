import webscrape

from bs4 import BeautifulSoup
import requests
import sys
import url from webscrape

url = 

headers = {'User-Agent':'Mozilla/5.0 '
            '(Windows NT 10.0; Win64; x64; rv:117.0) '
            'Gecko/20100101 Firefox/117.0'
           }
r = requests.get(url= url, headers= headers,verify= False) #temporary link
soup = BeautifulSoup(r.text, 'html.parser')

print(soup.prettify())

data = soup.find_all('')