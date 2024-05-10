import selenium
from bs4 import BeautifulSoup
import lxml
import requests
import re

response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
data_markup = response.text

soup = BeautifulSoup(data_markup, "lxml")
properties_list = soup.select(selector="#grid-search-results > ul > li")

address_list = []
rent_list = []
link_list = []

for prop in properties_list:
    address_list.append(prop.find(name="address").text.strip())

    rent_list.append(re.search(r'\$\d{1,3}(?:,\d{3})*(?:\.\d+)?', prop.select_one(
            selector="#zpid_2056905294 > div > div.StyledPropertyCardDataWrapper "
                     "> div.StyledPropertyCardDataArea-fDSTNn > div > span").text).group())

    link_list.append(prop.select_one(
        selector="#zpid_2056905294 > div > div.StyledPropertyCardDataWrapper > a"
    ).get("href"))

print(rent_list)
