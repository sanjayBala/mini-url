import json
from flask import Flask, render_template, request, jsonify, redirect, make_response, url_for
from forms import *
from main.parser import *

# init flask app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

shortner = URLShortener()
base_url = "https://sanjay-mini-url.herokuapp.com/"
protocol_prefix="https://"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shrtn', methods=['POST'])
def add_route():
    form = MainForm()
    original_url = str(form.original_url.data)
    print("Processing: " + original_url)
    shortened_url = shortner.processUrl(original_url)
    print("Shortened URL: " + str(shortened_url))
    print("Complete.")
    return render_template('result.html', original_url=original_url, shortened_url=base_url+shortened_url)

@app.route('/<string:shortened_url>', methods=['GET'])
def redirect_to_original(shortened_url):
    print("Processing...")
    original_url = shortner.redirectUrl(shortened_url)
    if original_url == None:
        print("Looks like this is an invalid short URL...")
        return redirect(url_for('error_not_found', error_message="Invalid Short URL, this Mapping is not present!"))
    original_url = str(original_url)
    print("Original URL: " + original_url)
    if protocol_prefix in original_url:
        return redirect(original_url)
    else:
        print("Appending protocol prefix... Redirecting...")
        return redirect(protocol_prefix + original_url)
    #return make_response(original_url, 302)

@app.route('/error', methods=['GET'])
def error_not_found(error_message="URL Mapping not found!!"):
    return render_template('error.html', error_message=error_message)

# @app.route('/list', methods=['GET'])
# def list_all():
#     all_values = listAll()
#     print("ALL VALUES SO FAR")
#     print(all_values)
#     return make_response(jsonify({"all_keys": all_values}), 200)

if __name__ == '__main__':
    app.run()