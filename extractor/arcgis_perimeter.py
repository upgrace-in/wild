import requests, os, csv, uuid, json
from bs4 import BeautifulSoup as bs
from datetime import datetime

from requests import exceptions
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
    d_url = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Current_WildlandFire_Perimeters/FeatureServer/0/query?where=1%3D1&outFields=poly_PolygonDateTime,poly_Acres_AutoCalc,irwin_FireCause,irwin_InitialLatitude,irwin_InitialLongitude,Shape__Area,Shape__Length,irwin_FSConfinePercent,irwin_IncidentName,irwin_IncidentShortDescription,irwin_PredominantFuelGroup&outSR=4326&f=json"
    r = requests.get(d_url, headers=hdr)
    d = json.loads(r.text)
    try:
        for i in d['features']:
            l = i['attributes']
            if (l['irwin_InitialLatitude'] == None) or (l['irwin_InitialLongitude'] == None):
                pass
            else:
                dt_obj = str(l['poly_PolygonDateTime'])
                if dt_obj != 'None':
                    dt_obj = ''.join(dt_obj.split())
                    dt_obj = datetime.utcfromtimestamp(int(dt_obj[:-3]))
                    current_date = datetime.now()
                    diff = current_date - dt_obj
                    if diff.days > 5:
                        pass
                    else:
                        save_it(['National Interagency Fire Center Perimeter', 'perimeter', uuid.uuid1().hex, 
                            l['irwin_InitialLatitude'], l['irwin_InitialLongitude'], str(dt_obj), l['irwin_IncidentName'], l['poly_Acres_AutoCalc'], l['irwin_FSConfinePercent'], l['irwin_FireCause'], l['irwin_IncidentShortDescription'], l['irwin_PredominantFuelGroup'], i['geometry']['rings'][0]])
        return "True"
    except Exception as e:
        return e