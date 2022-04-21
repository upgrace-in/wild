from django.contrib import admin
from django.urls import path, re_path
# from django.views.generic import TemplateView
from fire_alert_app import views
from scheduler import execute

urlpatterns = [
    # APIs
    path('get_all_object/', views.get_all_object, name="get_all_object"),
    path('get_all_red_flag_object/', views.get_all_red_object, name="get_all_red_object"),    
    
    path("change_password/", views.change_admin_pw, name='change_admin_pw'),
    path('get_object/', views.get_object, name="get_object"),
    path('delete_all/', views.delete_all, name="delete_all"),
    path('delete_all_objs/', views.delete_all_objs, name="delete_all_objs"),
    path('populate/', views.populate, name="populate"),
    path('alert/', views.alert, name="alert"),
    path('update/', views.update, name="update"),
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
]
