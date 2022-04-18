import requests
import uuid, os
import json
import bs4, html2text
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from fire_alert_app.views import save_it

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

data = []
url = "https://inciweb.nwcg.gov/feeds/maps/kml/"

path = os.path.abspath('.')
def take_out_file():
    r = requests.get(url, stream=True, headers=hdr)
    with open(path+'/static/files/inciweb.xml', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def remove_whitespaces(percentage):
    f_arr = []
    for i in percentage:
        if i == '':
            pass
        else:
            f_arr.append(i)
    return f_arr

def init():
    take_out_file()
    try:
        with open(path+'/static/files/inciweb.xml', 'r', encoding='utf-8') as f:
            da = f.read()
        Bs_data = BeautifulSoup(da, "xml")
        b_unique = Bs_data.find_all('Folder')
        for i in b_unique:
            b = i.find('description')
            
            percentage = b.text.split('contained.')[0].split('  ')
            f_percent = percentage[0].split('Incident')
            last_update = f_percent[0].replace('Last updated: ', '')
            percent = f_percent[1].split(' ')[2].split('%')[0]

            desc = b.text.split('contained.')[1]
            desc = desc.split('</p>View')[0].replace('</p>', ' ')
        
            h = html2text.HTML2Text()
            h.ignore_links = True
            desc = h.handle(desc)

            tm = last_update.split(',')[1].strip()
            if (i.find('latitude').text == None) or (i.find('longitude').text == None):
                pass
            else:
                if percent == "100":
                    pass
                else:
                    dt_obj = datetime.strptime(tm, '%d %b %Y %H:%M:%S')
                    n_t = datetime.now()
                    diff = n_t - dt_obj
                    if diff.days > 5:
                        pass
                    else:
                        save_it(['InciWeb', 'point', uuid.uuid1().hex,
                                        i.find('latitude').text,
                                        i.find('longitude').text,
                                        str(dt_obj),
                                        i.find('name').text,
                                        None,
                                        percent,
                                        None,
                                        desc,
                                        None,
                                        None])
        return "True"
    except Exception as e:
        return e