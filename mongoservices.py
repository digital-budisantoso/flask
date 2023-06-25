import pymongo
from pymongo import MongoClient
from flask import Flask,jsonify, request
import requests
import json

class mongoservices:
    def condb(self):
        uri = 'mongodb+srv://santosobudiaris:admin123@cluster0.alb1oiq.mongodb.net/?retryWrites=true&w=majority'
        # create client
        client = MongoClient(uri)
        db = client.transportdb
        return db
        
    def save_sample(self, data):
        try:
            db = mongoservices.condb(self)
            samples_coll = db.samples
            samples_coll.insert_one(data)
            return jsonify({"code":"1","status":"success"})
        except Exception as ex:
            return jsonify({"code":"0","status":ex})
            
    def save_smpl(self, data):
        try:
            url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-qkomj/endpoint/data/v1/action/insertOne"
            payload = json.dumps({
                "collection": "samples",
                "database": "transportdb",
                "dataSource": "Cluster0",
                "document" :   data 
                })
            headers = {
                'Content-Type': 'application/json',
                'Access-Control-Request-Headers': '*',
                'api-key': 'e0jbexwy3urdiuizdL9BlPIMQbkhCI6OaispZnyMXk5H6gvstdUJILNjo54vqRJN'
                }
            response = requests.request("POST", url, headers=headers, data=payload)
            return jsonify({"code":"1","status":requests.text})
        except Exception as ex:
            return jsonify({"code":"0","status":ex})