import sys
import random
from flask import Flask, render_template, jsonify, request
import openrouteservice
from geopandas import *
from geopy import *
import requests
import json

class mapservices:
    def getpath(self,src,dst):
        #locator = Nominatim(user_agent="myGeocoder")
        #loc_1 = locator.geocode(src)
        #loc_2 = locator.geocode(dst)
        loc_1 = mapservices.findlocation(self, src)
        loc_2 = mapservices.findlocation(self, dst)
        client = openrouteservice.Client(key='5b3ce3597851110001cf62485a8c0921cbaf44df88efb9f625321c1a')
        #coords = ((loc_1.longitude,loc_1.latitude),(loc_2.longitude,loc_2.latitude))
        coords = ((float(loc_1['lon']),float(loc_1['lat'])),(float(loc_2['lon']),float(loc_2['lat'])))
        res = client.directions(coords)
        geometry = client.directions(coords)['routes'][0]['geometry']
        summary = res['routes'][0]['summary']
        decoded = openrouteservice.convert.decode_polyline(geometry)
        return jsonify({"data": decoded['coordinates'],"query":[[float(loc_1['lon']),float(loc_1['lat'])],[float(loc_2['lon']),float(loc_2['lat'])]],"summary":[summary['distance'],summary['duration']]})

    def findlocation(self,place):
        url = "https://nominatim.openstreetmap.org/search?q="+place+"&format=json&limit=1"
        res4 = requests.get(url=url)
        con = res4.content
        jc = json.loads(con.decode("utf-8"))
        if len(jc)>0:
           return jc[0]
        else:
           return null