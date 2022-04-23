from django.shortcuts import redirect, render, HttpResponse
from django.http import JsonResponse
from httplib2 import Http
from fire_alert_app.models import Data, red_flag_data_model
import uuid
import csv
import os
import math
import json
import time
from django.views.decorators.csrf import csrf_exempt
from ast import literal_eval
from django.core import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

path = os.path.abspath('.')


def index(request):
    return render(request, 'index.html')


def put_red_label_data(arr):
    try:
        if(arr == 'delete_all'):
            red_flag_data_model.objects.all().delete()
            return True
        else:
            for i in arr:
                m = red_flag_data_model.objects.create(
                    desc=i['summary'],
                    polygon=i['cap:geocode']['value'][1],
                    date_time=i['cap:effective']
                )
                m.save()
            return True
    except EOFError as e:
        print(e)
        return False


@csrf_exempt
def get_all_red_object(request):
    if request.method == 'POST':
        m = red_flag_data_model.objects.all()
        s = serializers.serialize("json", m)
        return HttpResponse(s)
    else:
        return HttpResponse("Method Not Allowed !")


def change_admin_pw(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        old_pass = request.POST['old_pass']
        new_pass = request.POST['new_pass']
        u = User.objects.filter(is_superuser=True)
        try:
            for i in u:
                if i.username == uname:
                    if i.check_password(old_pass):
                        u = User.objects.get(username=uname)
                        u.set_password(new_pass)
                        u.save()
                    else:
                        return HttpResponse("Wrong Password :/")
            return HttpResponse("Password Changed :) <br> <a href='/admin/'>Login Here</a>")
        except EOFError:
            return HttpResponse("User not found :/")
    else:
        return render(request, "change.html")


@csrf_exempt
def get_all_object(request):
    if request.method == 'POST':
        m = Data.objects.all()
        s = serializers.serialize("json", m)
        return HttpResponse(s)
    else:
        return HttpResponse("Method Not Allowed !")


@csrf_exempt
def get_object(request):
    if request.method == 'POST':
        try:
            m = Data.objects.get(reference_id=request.POST['reference_id'])
            m = {'data_source_name': m.data_source_name,
                 'data_source_type': m.data_source_type,
                 'reference_id': m.reference_id,
                 'latitude': m.latitude,
                 'longitude': m.longitude,
                 'time_date': m.time_date,
                 'name': m.name,
                 'acreage': m.acreage,
                 'percent': m.percent,
                 'cause': m.cause,
                 'description': m.description,
                 'primary': m.primary,
                 'perimeter': m.perimeter,
                 'datetime': m.datetime,
                 }
            return JsonResponse(m)
        except ObjectDoesNotExist:
            return HttpResponse("Not Found")
    else:
        return HttpResponse("Method Not Allowed !")


def delete_all_objs():
    try:
        Data.objects.all().delete()
        return HttpResponse("All")
    except EOFError as e:
        return HttpResponse(e)


def delete_all(request):
    m = Data.objects.all()
    while Data.objects.count():
        m[0].delete()
    return redirect('populate')


def check_for_the_shortest_miles(arr):
    min_v = arr[0][0]
    i = None
    for i in range(0, len(arr)):
        if(arr[i][0] < min_v):
            min_v = arr[i][0]
    return i


def check_for_the_shortest_distance(arr):
    min = arr[0][0]
    ref = arr[0][1]
    for i in range(0, len(arr)):
        if(arr[i][0] < min):
            min = arr[i][0]
            ref = arr[i][1]
    return ref


def formula(x2, initLat, y2, initLong):
    d = ((((x2 - initLat)**2) + ((y2-initLong)**2))**0.5)
    return d


def give_in_miles(initLat, initLong, endingLat, endingLong):
    initLat = math.radians(initLat)
    initLong = math.radians(initLong)
    endingLat = math.radians(endingLat)
    endingLong = math.radians(endingLong)
    distance = (2*6371)*(math.asin(math.sqrt(math.pow(math.sin((endingLat-initLat)/2), 2) +
                                             math.cos(initLat)*math.cos(endingLat)*math.pow(math.sin((endingLong-initLong)/2), 2))))
    distanceInMiles = distance*0.621371
    return distanceInMiles


@csrf_exempt
def alert(request):
    if request.method == 'POST':
        # Step 1 : arr of objects
        m = Data.objects.all()

        # Step 2 : User's Latitude Longitude & Radius
        initLat = float(request.POST['latitude'])
        initLong = float(request.POST['longitude'])
        radius = float(request.POST['radius'])

        # Step 3 : Using distance formula for every objects (Lat, Long)
        distance_arr = []
        for i in m:
            if i.data_source_type == 'perimeter':
                arr = literal_eval(i.perimeter)
                for l in arr:
                    x2 = float(l[0])
                    y2 = float(l[1])
                    d = formula(x2, initLat, y2, initLong)
                    distance_arr.append([d, i.reference_id])
            else:
                if i.latitude != "":
                    x2 = float(i.latitude)
                    y2 = float(i.longitude)
                    d = formula(x2, initLat, y2, initLong)
                    distance_arr.append([d, i.reference_id])

        shortest_one = check_for_the_shortest_distance(distance_arr)

        # Fetching the shortest_one from database
        m = Data.objects.get(reference_id=shortest_one)

        if m.data_source_type == 'perimeter':
            miles_arr = []
            arr = literal_eval(m.perimeter)
            for l in arr:
                endLat = float(l[0])
                endLong = float(l[1])
                distanceInMiles = give_in_miles(
                    initLat, initLong, endLat, endLong)
                miles_arr.append([distanceInMiles, endLat, endLong])
            shortest_miles = check_for_the_shortest_miles(miles_arr)
            f_str = {"distance": str(miles_arr[shortest_miles][0]),
                     "latitude": str(miles_arr[shortest_miles][1]),
                     "longitude": str(miles_arr[shortest_miles][2]),
                     "reference_id": str(m.reference_id)}
        else:
            endingLat = float(m.latitude)
            endingLong = float(m.longitude)
            distanceInMiles = give_in_miles(
                initLat, initLong, endingLat, endingLong)
            f_str = {"distance": str(distanceInMiles),
                     "latitude": str(m.latitude),
                     "longitude": str(m.longitude),
                     "reference_id": str(m.reference_id)
                     }
        return JsonResponse(f_str, safe=False)
    else:
        return HttpResponse("Method Not Allowed")


def updated_logs(msg):
    with open("logs", "a") as f:
        f.write(str(msg))
        f.close()


def save_it(i):
    try:
        m = Data.objects.create(
            data_source_name=i[0],
            data_source_type=i[1],
            reference_id=i[2],
            latitude=i[3],
            longitude=i[4],
            time_date=i[5],
            name=i[6],
            acreage=i[7],
            percent=i[8],
            cause=i[9],
            description=i[10],
            primary=i[11],
            perimeter=i[12]
        )
        m.save()
        return True
    except EOFError:
        return False


@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = request.POST['data']
        # dlt = request.POST['type']
        # Data.objects.filter(data_source_name=dlt).delete()
        data = json.loads(data)
        for i in data:
            save_it(i)
        return HttpResponse("Updated")
    else:
        return HttpResponse("Method Not Allowed")


def populate(request):
    if request.method == 'POST':
        i = ['InciWeb', 'point', uuid.uuid1().hex,
                        request.POST['latitude'],
                        request.POST['longitude'],
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None]
        save_it(i)
        return render(request, 'populate.html')
    else:
        return render(request, 'populate.html')
