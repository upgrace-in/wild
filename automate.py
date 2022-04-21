from extractor import arcgis_location, arcgis_perimeter, fsapps, inciweb, nasa, red_flag
from fire_alert_app.views import update, updated_logs, delete_all_objs, put_red_label_data


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

    msg = put_red_label_data('delete_all')
    if msg == True:
        m = red_flag.init()
        updated_logs(m)
