import requests, json, uuid, os
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile
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

url = "https://fsapps.nwcg.gov/data/kml/conus_lg_incidents.kmz"
path = os.path.abspath('.')
def take_out_file():
    r = requests.get(url, stream=True, headers=hdr)
    with open(path+'/static/files/'+url.split('/')[-1], 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)

def init():
    take_out_file()
    kmz = ZipFile(path+'/static/files/conus_lg_incidents.kmz', 'r')
    doc = kmz.open("conus_lg_incidents.kml", 'r').read()
    kml_soup = bs(doc, 'lxml-xml')
    placemark = kml_soup.find_all('Placemark')
    try:
        for i in placemark:
            p = i.find('description').text.replace('</b>', '')
            p = p.replace('<b>', '')
            p = p.replace('See http://', 'http://')
            p = p.replace('.pdf for more information', '.pdf')
            f = p.replace(' ', '').split('<br/>')
            if (f[1].split(':')[1] == None) or (f[2].split(':')[1] == None):
                pass
            else:
                date_obj = f[0].split(':')[1]
                dt_obj = datetime.strptime(date_obj, '%m/%d/%Y')
                n_t = datetime.now()
                diff = n_t - dt_obj
                if diff.days > 5:
                    pass
                else:
                    save_it(['USDA Forest Service', 'point', uuid.uuid1().hex,
                                    f[1].split(':')[1],
                                    f[2].split(':')[1],
                                    str(dt_obj),
                                    i.find('name').text,
                                    f[4].split(':')[1].split('acres')[0],
                                    f[5].split(':')[1].split('%')[0],
                                    None,
                                    f[-1],
                                    None,
                                    None])
        return "True"
    except Exception as e:
        return e