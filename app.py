import json
from flask import Flask, render_template, request, jsonify, make_response
from main.parser import *

# init flask app
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten/<string:incoming_url>', methods=['POST'])
def add_route(incoming_url):
    print("Processing...")
    original_url, shortened_url = processUrl(incoming_url)
    print("URL: " + str(shortened_url))
    print("Complete.")
    return render_template('result.html', original_url=original_url, shortened_url=shortened_url)

@app.route('/<string:incoming_url>', methods=['POST'])
def shorten_another(incoming_url):
    print("Processing...")
    original_url, shortened_url = processUrl(incoming_url)
    print("URL: " + str(encoded_url))
    print("Complete.")
    return make_response(shortened_url, 302)


if __name__ == '__main__':
    app.run()