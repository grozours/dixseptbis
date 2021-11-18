#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import requests
import deezer
import getpass

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

radio_url = "https://www.radioking.com/widgets/player/player.php?id=444"

# Create application deezer token from https://developers.deezer.com/myapps
DEEZER_AUTH_PAGE="https://connect.deezer.com/oauth/auth.php?"
DEEZER_TOKEN_PAGE="https://connect.deezer.com/oauth/access_token.php?"

DEEZER_APP_ID=""
DEEZER_APP_SECRET=""
DEEZER_REDIRECT_URL=""



code_page= DEEZER_AUTH_PAGE+"app_id="+DEEZER_APP_ID+"&redirect_uri="+DEEZER_REDIRECT_URL+"&perms=basic_access"
code_result = requests.get(code_page)
print(f'\n Click on link to get your Deezep App Code :\n {code_result.url} \n')
DEEZER_CODE = getpass.getpass(" Deezer App Code :")

DEEZER_TOKEN_URL = DEEZER_TOKEN_PAGE+"app_id="+DEEZER_APP_ID+"&secret="+DEEZER_APP_SECRET+"&code="+DEEZER_CODE
token_result = requests.get(DEEZER_TOKEN_URL)
DEEZER_TOKEN = (token_result.text.split("&expires")[0]).split("access_token=")[1]

dz_client = deezer.Client(access_token=DEEZER_TOKEN)

def get_title(webpage):
    driver.get(webpage)
    artiste = driver.find_element(By.ID,"artiste")
    titre = driver.find_element(By.ID,"titre")
    return artiste.text, titre.text

def get_refreshed_page():
    driver.refresh()
    artiste = driver.find_element(By.ID,"artiste")
    titre = driver.find_element(By.ID,"titre")
    return artiste.text, titre.text

def get_time():
    now = datetime.now()
    return now.strftime("%Y%m%d-%H%M%S")

print(f'\n Radio 17Bis Playlist :\n')


artiste,titre=get_title(radio_url)
deezer_song_url=dz_client.search(query=titre,artist=artiste,track=titre)[0].link
print(f' {get_time()} : {artiste} - {titre} - {deezer_song_url}')

old_artiste=artiste
old_titre=titre

while True:
    time.sleep(20)
    artiste,titre = get_refreshed_page()
    if artiste != old_artiste and old_titre is not None and old_titre != titre and "17bis" not in artiste:
       deezer_song_url=dz_client.search(query=titre,artist=artiste,track=titre)[0].link
       print(f' {get_time()} : {artiste} - {titre} - {deezer_song_url}')
       old_artiste=artiste
       old_titre=titre
       
