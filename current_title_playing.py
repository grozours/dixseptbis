#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

url = "https://www.radioking.com/widgets/player/player.php?id=444"
driver.get(url)

artiste = driver.find_element(By.ID,"artiste")
titre = driver.find_element(By.ID,"titre")
print(f'{artiste.text} - {titre.text}')
