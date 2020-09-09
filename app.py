import json
from flask import Flask, render_template, request, jsonify, make_response
from main.parser import *

# init flask app
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
    return "Hey, I am a URL Shortener Service."

@app.route('/shorten', methods=['POST'])
def shorten():
    if request.is_json() == False:
        print("Hey! This ain't a JSON.")
        return make_response(jsonify({'error': 'Bad Request'}), 400)
    else:
        print("Processing...")
        encoded_url={ 'data': insertUrl(request.json.incoming_url)}
        print("Complete.")
        return jsonify(encoded_url)


if __name__ == '__main__':
    app.run()