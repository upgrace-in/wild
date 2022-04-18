import requests, os, csv, uuid, json
from bs4 import BeautifulSoup as bs
from datetime import date, datetime
import pytz, tzlocal
from fire_alert_app.views import save_it

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

path = os.path.abspath('.')
data =  []

def init():
    try:
        d_url = "https://opendata.arcgis.com/datasets/9838f79fb30941d2adde6710e9d6b0df_0.geojson"
        r = requests.get(d_url, stream=True, headers=hdr)
        f = open(path+'/static/files/locations.json', 'wb')
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
        f = open(path+'/static/files/locations.json',)
        d = json.loads(f.read())
        for i in d['features']:
            l = i['properties']
            if (l['InitialLatitude'] == None) or (l['InitialLongitude'] == None):
                pass
            else:
                d = l['FireDiscoveryDateTime'].split('T')
                dat = d[0].split('-')
                tm = d[1].split('Z')[0].split(':')
                then = datetime(int(dat[0]), int(dat[1]), int(dat[2]), int(tm[0]), int(tm[1]), int(tm[2]))
                now  = datetime.now()             
                duration = now - then
                if duration.days > 5:
                    pass
                else:
                    save_it(['National Interagency Fire Center Locations', 'point', uuid.uuid1().hex, 
                        l['InitialLatitude'], l['InitialLongitude'], str(then), l['IncidentName'], l['CalculatedAcres'], l['PercentContained'], l['FireCause'], l['IncidentShortDescription'], l['PredominantFuelGroup'], None])
        return "True"
    except Exception as e:
        return e