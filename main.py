from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Hallo": "Welcome to your Flask Application"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
