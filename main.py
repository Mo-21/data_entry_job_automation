from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
import requests
import re
import time

response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
data_markup = response.text

soup = BeautifulSoup(data_markup, "lxml")
properties_list = soup.select(selector="#grid-search-results > ul > li")

properties_details = {}

for index, prop in enumerate(properties_list):
    address = prop.find(name="address").text.strip()
    link = prop.select_one(
        selector="#zpid_2056905294 > div > div.StyledPropertyCardDataWrapper > a"
    ).get("href")
    rent = re.search(r'\$\d{1,3}(?:,\d{3})*(?:\.\d+)?', prop.select_one(
        selector="#zpid_2056905294 > div > div.StyledPropertyCardDataWrapper "
                 "> div.StyledPropertyCardDataArea-fDSTNn > div > span").text).group()

    properties_details[index] = {
        "address": address,
        "rent": rent,
        "link": link
    }

# Submitting form with selenium

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)

driver = webdriver.Chrome(chrome_options)

for n in range(len(properties_details)):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfUeIWzDkY6VlAAL-hUN-d8zouYGBnnJ9yXDisNj7qr6c3-nw/viewform")

    address_input = driver.find_element(
        by="xpath",
        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )

    rent_input = driver.find_element(
        by="xpath",
        value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )

    link_input = driver.find_element(
        by="xpath",
        value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )

    submit = driver.find_element(
        by="xpath",
        value='/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span')

    time.sleep(5)

    address_input.send_keys(properties_details[n]["address"])
    rent_input.send_keys(properties_details[n]["rent"])
    link_input.send_keys(properties_details[n]["link"])
    submit.click()

driver.close()
