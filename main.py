from flask import Flask, jsonify
import os
import mongoservices

app = Flask(__name__)
mongosvc = mongoservices.mongoservices()

@app.route('/')
def index():
    return jsonify({"Hallo": "Welcome to your Flask Application"})

@app.route('/api/menu')
def menu():
    return jsonify({"code": "1", "status": "OK", "menus":"menus"})

@app.route('/api/samples', methods=['POST'])
def save_sample():
    data = request.json
    return mongosvc.save_smpl(data)	


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
