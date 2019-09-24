# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 16:18:08 2019

@author: Simon
"""

import geopy.distance
import csv
import requests
import time

def getVar(obj,x,y=None,z=None):
    try:
        if y is not None:
            if z is not None:
                return obj[x][y][z]
            else:
              return obj[x][y]
        else:
            return obj[x]
    except Exception as e:
        return ' '
    
    
def writeObj(results):
    for obj in results:
        name=getVar(obj,'name')
        location_lat=getVar(obj,'geometry','location','lat')
        location_lng=getVar(obj,'geometry','location','lng')
        rating=getVar(obj,'rating')
        rating_count=getVar(obj,'user_ratings_total')
        obj_type=getVar(obj,'types')
        obj_id=getVar(obj,'place_id')
        price=getVar(obj,'price_level')
        vicinity=getVar(obj,'vicinity')
        closed=getVar(obj,'permanently_closed')
        photo_id=getVar(obj,'photos',0,'photo_reference')
        try:
            writer.writerow([name,location_lat,location_lng,rating,rating_count,obj_type,obj_id,price,vicinity,closed,photo_id])
        except:
            writer.writerow(['','','','','','','','','','',''])
    return obj

center=(lng,lat)
key='api-key'
types = ("accounting", "airport", "amusement_park", "aquarium", "art_gallery", "atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store", "book_store", "bowling_alley", "bus_station", "cafe", "campground", "car_dealer", "car_rental", "car_repair", "car_wash", "casino", "cemetery", "church", "city_hall", "clothing_store", "convenience_store", "courthouse", "dentist", "department_store", "doctor", "electrician", "electronics_store", "embassy", "fire_station", "florist", "funeral_home", "furniture_store", "gas_station", "gym", "hair_care", "hardware_store", "hindu_temple", "home_goods_store", "hospital", "insurance_agency", "jewelry_store", "laundry", "lawyer", "library", "liquor_store", "local_government_office", "locksmith", "lodging", "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater", "moving_company", "museum", "night_club", "painter", "park", "parking", "pet_store", "pharmacy", "physiotherapist", "plumber", "police", "post_office", "real_estate_agency", "restaurant", "roofing_contractor", "rv_park", "school", "shoe_store", "shopping_mall", "spa", "stadium", "storage", "store", "subway_station", "supermarket", "synagogue", "taxi_stand", "train_station", "transit_station", "travel_agency", "veterinary_care", "zoo")

for type in types:
    print(type)
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(center[0])+','+str(center[1])+'&type='+type+'&radius=5000&key='+key
    headers={'content-type':'application/json',
             'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'}
    
    with open(type+'.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["name","lat","long","rating","ratings","types","id","price","vicinity","closed","photo"])  
        
        response = requests.get(url=url, headers=headers).json()
        if len(response['results'])>0:
            obj=writeObj(response['results'])
        coords = (getVar(obj,'geometry','location','lat'),getVar(obj,'geometry','location','lng'))
        print(geopy.distance.geodesic(center, coords).m)
        
        while 'next_page_token' in response:
            token=response['next_page_token']
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken='+token+'&key='+key
            time.sleep(2)
            response = requests.get(url=url, headers=headers).json()
            if len(response['results'])>0:
                obj=writeObj(response['results'])
            coords = (getVar(obj,'geometry','location','lat'),getVar(obj,'geometry','location','lng'))
            print(geopy.distance.geodesic(center, coords).m)
            
            
    csvfile.close()