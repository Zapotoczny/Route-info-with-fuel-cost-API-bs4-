# importing the libraries
from bs4 import BeautifulSoup
import requests
import re

url="https://www.autocentrum.pl/paliwa/ceny-paliw/"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

def get_prices(type):
    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    results = soup.find_all('div', {'class': 'price'})
    desired_result = results[2]
    prices = []
    for resault in results:
        for x in resault:
            prices.append(float(re.findall("\d+\,\d+",x)[0].replace(',','.')))
            break

    resault = {
        '95': prices[0],
        '98': prices[1],
        'on': prices[2],
        'on_plus': prices[3],
        'lpg': prices[4],
    }

    return resault[type]