from django.contrib import admin
from django.db.models.fields import DateTimeField
from fire_alert_app.models import Data, red_flag_data_model

class DataAdmin(admin.ModelAdmin):
    search_fields=('data_source_name',)
    readonly_fields = ('datetime',)

admin.site.register(Data, DataAdmin)
admin.site.register(red_flag_data_model)