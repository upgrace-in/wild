import requests
import csv
import uuid
import json
import os
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pytz
import math
import geopy.distance
from fire_alert_app.views import save_it

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

url = "https://firms.modaps.eosdis.nasa.gov"

files = []
data = []
raw_dataset = []
final_dataset = []

path = os.path.abspath('.')


def give_in_miles(x1, y1, x2, y2):
    coords_1 = (x1, y1)
    coords_2 = (x2, y2)
    return geopy.distance.geodesic(coords_1, coords_2).miles


def take_out_file(data):
    d_url = url+data
    name_of_file = data.split('/')[-1]
    files.append(name_of_file)
    r = requests.get(d_url, stream=True, headers=hdr)
    with open(path+'/static/files/'+name_of_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def get_files():
    s = requests.Session()
    p = s.get(url+"/active_fire/#firms-txt", headers=hdr)
    soup = bs(p.content, 'html.parser')
    table = soup.find(id="active-fire-text")
    tr = table.find_all('tr')[3:5]  
    for i in tr:
        td = i.find_all('td')
        for j in td:
            a = j.find_all('a')
            for k in a:
                if (k.text == '24h') and ("MODIS" in k['href']):
                    take_out_file(k['href'])


def save_the_arr():
    for i in final_dataset:
        save_it(['FIRMS', 'point', uuid.uuid1().hex, i[0], i[1],
                i[2], None, None, None, None, None, None, None])


def calculations(x1, y1, d1, x2, y2, d2):
    d = give_in_miles(x1, y1, x2, y2)
    if d <= 3: # Change the mile here
        lat = (x1+y1)/2
        long = (x2+y2)/2
        final_dataset.append([lat, long, d1])
    else:
        final_dataset.append([x1, y1, d1])
        final_dataset.append([x2, y2, d2])


def sort_the_arr():
    raw = sorted(raw_dataset, key=lambda x: x[1], reverse=True)
    length = len(raw)
    if (length % 2) != 0:
        raw.append([0, 0, 0])
        raw.append([0, 0, 0])
        length += 2
    i = 0
    length -= 1
    while(i < length):
        calculations(float(raw[i][0]), float(raw[i][1]), str(raw[i][2]),
                     float(raw[i+1][0]), float(raw[i+1][1]), str(raw[i+1][2]))
        i += 2
    save_the_arr()


def init():
    raw_dataset.clear()
    files.clear()
    data.clear()
    raw_dataset.clear()
    final_dataset.clear()
    get_files()
    try:
        for i in files:
            with open(path+'/static/files/'+i) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        d_t = datetime.strptime(row[5], '%Y-%m-%d')
                        n_t = datetime.now()
                        diff = n_t - d_t
                        if diff.days > 1:
                            pass
                        else:
                            raw_dataset.append([row[0], row[1], str(d_t)])
        len(raw_dataset)
        sort_the_arr()
        return "True"
    except Exception as e:
        return e