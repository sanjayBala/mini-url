import json
from flask import Flask, render_template, request, jsonify, make_response
from main.parser import *

# init flask app
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
    return "Hey, I am a URL Shortener Service."

@app.route('/shorten/<string:incoming_url>', methods=['POST'])
def shorten(incoming_url):
    print("Processing...")
    shortened_url=processUrl(incoming_url)
    print("URL: " + str(shortened_url))
    print("Complete.")
    return make_response(jsonify({'Shortened URL': shortened_url}), 200)

@app.route('/r/<string:incoming_url>', methods=['POST'])
def shorten(incoming_url):
    print("Processing...")
    encoded_url=processUrl(incoming_url)
    print("URL: " + str(encoded_url))
    print("Complete.")
    return make_response(encoded_url, 302)


if __name__ == '__main__':
    app.run()