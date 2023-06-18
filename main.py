from flask import Flask, jsonify, request
import os
import mongoservices
import mapservices

app = Flask(__name__)
mongosvc = mongoservices.mongoservices()
mapsvc = mapservices.mapservices()

@app.route('/')
def index():
    return jsonify({"Hallo": "Welcome to your Flask Application"})

@app.route('/api/menu')
def menu():
    return jsonify({"code": "1", "status": "OK", "menus":"menus"})

@app.route('/api/samples', methods=['POST'])
def save_sample():
    data = request.json
    return mongosvc.save_sample(data)	

@app.route('/api/findplace', methods=['GET'])
def find_place():
    args = request.args
    qry = args.get("qry")
    return mapsvc.findplace(qry)

@app.route('/api/route', methods=['POST'])
def find_route():
    data = request.json
    loc_1 = data.get('src')
    loc_2 = data.get('dst')
    return mapsvc.findroute(loc_1, loc_2)
	
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
