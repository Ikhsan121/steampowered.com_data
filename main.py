import os
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time

URL = "https://store.steampowered.com/search/?term=gta"

service = Service(executable_path="C:\Development\chromedriver.exe")
options = Options()
options.add_argument('--incognito')
options.add_argument('start-maximized')
driver = webdriver.Chrome(service=service, options=options)

driver.get(URL)
SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

contents = soup.find('div', id="search_resultsRows")
games = contents.find_all('a')
result = []
# scraping process
for game in games:
    link = game['href']
    title = game.find('span', class_="title").text
    price = game.find('div', class_="search_price").text.strip()
    released = game.find('div', class_="search_released").text.strip()

    if released == "":
        released = None
    if price == "":
        price = None

    final_data = {
        'title': title,
        'price': price,
        'link': link,
        "released": released,
    }
    result.append(final_data)

try:
    os.mkdir('json_result')
except FileExistsError:
    pass
with open('json_result/final_data.json', "w+") as json_data:
    json.dump(result, json_data)
print('json created')

# create csv
df = pd.DataFrame(result)
df.to_csv('steampowered_data.csv', index=False)
df.to_excel('steampowered_data.xlsx', index=False)
print("Data created success")
print("Total rows", len(result))