import xmltodict
import requests
import os
import csv
import uuid
import json
from bs4 import BeautifulSoup as bs
from datetime import date, datetime
import pytz
import tzlocal
from xml.etree import ElementTree
from fire_alert_app.views import put_red_label_data

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

path = os.path.abspath('.')
filtered_data = []

def init():
    d_url = "https://alerts.weather.gov/cap/us.php?x=0"
    try:
        r = requests.get(d_url, headers=hdr)
        data = xmltodict.parse(r.content)
        for i in data['feed']['entry']:
            if 'Red Flag Warning' in i['cap:event']:
                filtered_data.append(i)
        put_red_label_data(filtered_data)
        return True
    except EOFError:
        return False