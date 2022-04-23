from extractor import arcgis_location, arcgis_perimeter, fsapps, inciweb, nasa, red_flag
from fire_alert_app.views import update, delete_all_objs, put_red_label_data
from fire_alert import settings


def start():

    if settings.DEBUG == True:

        msg = put_red_label_data('delete_all')
        if msg == True:
            red_flag.init()

    else:
        d = delete_all_objs()
        

        msg = arcgis_perimeter.init()
            

        msg = arcgis_location.init()
            

        msg = fsapps.init()
            

        msg = inciweb.init()
            

        msg = nasa.init()
            

        msg = put_red_label_data('delete_all')
        if msg == True:
            m = red_flag.init()
            
