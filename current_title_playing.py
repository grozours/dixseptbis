#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import requests
import deezer
import getpass

# Headless firefor for less ressources
# killall firefox when stopping script
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

# Webradio scrapped
RADIO_URL = "https://www.radioking.com/widgets/player/player.php?id=444"

# Deezer oAuth URLs used
DEEZER_AUTH_PAGE="https://connect.deezer.com/oauth/auth.php?"
DEEZER_TOKEN_PAGE="https://connect.deezer.com/oauth/access_token.php?"
# Create application deezer token from https://developers.deezer.com/myapps
DEEZER_APP_ID=""
DEEZER_APP_SECRET=""
DEEZER_REDIRECT_URL=""

def get_first_content(webpage):
    driver.get(webpage)

def get_refreshed_page():
    driver.refresh()

def get_song_info():
    artiste = driver.find_element(By.ID,"artiste")
    titre = driver.find_element(By.ID,"titre")
    return artiste.text, titre.text

def get_time():
    now = datetime.now()
    return now.strftime("%Y%m%d-%H%M%S")

def deezer_song_url(artiste,titre):
    return (dz_client.search(query=titre,artist=artiste,track=titre))[0].link


# Getting through oAuth Deezer process
code_page= DEEZER_AUTH_PAGE+"app_id="+DEEZER_APP_ID+"&redirect_uri="+DEEZER_REDIRECT_URL+"&perms=basic_access"
code_result = requests.get(code_page)
print(f'\n Click on link to get your Deezep App Code :\n {code_result.url} \n')
DEEZER_CODE = getpass.getpass(" Deezer App Code :")

DEEZER_TOKEN_URL = DEEZER_TOKEN_PAGE+"app_id="+DEEZER_APP_ID+"&secret="+DEEZER_APP_SECRET+"&code="+DEEZER_CODE
token_result = requests.get(DEEZER_TOKEN_URL)
DEEZER_TOKEN = (token_result.text.split("&expires")[0]).split("access_token=")[1]

# Use token with deezer python client
dz_client = deezer.Client(access_token=DEEZER_TOKEN)


print(f'\n Radio 17Bis Playlist :\n')

get_first_content(RADIO_URL)
artiste,titre = get_song_info()
print(f' {get_time()} : {artiste} - {titre} - {deezer_song_url(artiste,titre)}')

old_artiste=artiste
old_titre=titre

while True:
    time.sleep(20)
    get_refreshed_page()
    artiste,titre = get_song_info()
    if artiste != old_artiste and old_titre is not None and old_titre != titre and "17bis" not in artiste:
       print(f' {get_time()} : {artiste} - {titre} - {deezer_song_url(artiste,titre)}')
       old_artiste=artiste
       old_titre=titre
       
