from extractor import arcgis_location, arcgis_perimeter, fsapps, inciweb, nasa
from fire_alert_app.views import update, updated_logs, delete_all_objs


def start():

    d = delete_all_objs()
    updated_logs(d)
    
    msg = arcgis_perimeter.init()
    if msg != 'True':
        updated_logs(msg)

    msg = arcgis_location.init()
    if msg != 'True':
        updated_logs(msg)

    msg = fsapps.init()
    if msg != 'True':
        updated_logs(msg)

    msg = inciweb.init()
    if msg != 'True':
        updated_logs(msg)

    msg = nasa.init()
    if msg != 'True':
        updated_logs(msg)
