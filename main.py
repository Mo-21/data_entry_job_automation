import selenium
from bs4 import BeautifulSoup
import lxml
import requests

response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
data_markup = response.text

soup = BeautifulSoup(data_markup, "lxml")
properties_list = soup.select(selector="#grid-search-results > ul > li")

properties_details = {
    index: {
        "address": prop.find(name="address").text.strip(),
        "rent": prop.select_one(
            selector="#zpid_2056905294 > div > div.StyledPropertyCardDataWrapper "
                     "> div.StyledPropertyCardDataArea-fDSTNn > div > span").text.strip(),
        "link": prop.select_one(selector="#zpid_2056905294 > div > div.StyledPropertyCardDataWrapper > a").get("href")
    }

    for index, prop in enumerate(properties_list)
}

print(properties_details)
