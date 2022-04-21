from django.db import models
import datetime
class Data(models.Model):
    data_source_name = models.CharField(max_length=200, null=True, blank=True)
    data_source_type = models.CharField(max_length=200, null=True, blank=True)
    reference_id = models.CharField(max_length=1000)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)
    time_date = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    acreage = models.CharField(max_length=200, null=True, blank=True)
    percent = models.CharField(max_length=200, null=True, blank=True)
    cause = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    primary = models.CharField(max_length=200, null=True, blank=True)
    perimeter = models.CharField(max_length=200, null=True, blank=True) 
    datetime = models.DateTimeField(auto_now_add=datetime.datetime.now(), editable=True)

    def __str__(self):
        return self.data_source_name

class red_flag_data_model(models.Model):
    desc = models.CharField(max_length=2000, null=True, blank=True)
    polygon = models.CharField(max_length=2000, null=True, blank=True)
    date_time = models.CharField(max_length=2000)
