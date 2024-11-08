import os
from dhooks import Webhook, Embed, File
import requests
import logging
from datetime import datetime
import time
import shutil


from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import requests 
import json
from time import sleep
from discordwebhook import Discord
import pyimgur
import os
import sys
from pytz import timezone, utc

url = 'https://museum-tickets.nintendo.com/en/api/calendar?target_year=2024&target_month=12'
HEADERS = {'x-requested-with': 'XMLHttpRequest'}

#  Making a get request 
response = requests.get(url, headers= HEADERS) 
# print response 
urlResponseCode = response.status_code 
urlResponse = response.text

print("urlResponse:")
print(urlResponse)