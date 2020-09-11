import json
from flask import Flask, render_template, request, jsonify, redirect, make_response
from forms import *
from main.parser import *

# init flask app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shrtn', methods=['POST'])
def add_route():
    form = MainForm()
    original_url = str(form.original_url.data)
    print("Processing..." + original_url)
    a, shortened_url = processUrl(original_url, 1287)
    print("URL: " + str(shortened_url))
    print("Complete.")
    return render_template('result.html', original_url=original_url, shortened_url=shortened_url)

@app.route('/<string:shortened_url>', methods=['GET'])
def redirect_to_original(shortened_url):
    print("Processing...")
    original_url = str(getUrl(shortened_url))
    print("URL: " + original_url)
    print("Complete.")
    output = {"data": original_url}
    return redirect(original_url)
    #return make_response(original_url, 302)

# @app.route('/list', methods=['GET'])
# def list_all():
#     all_values = listAll()
#     print("ALL VALUES SO FAR")
#     print(all_values)
#     return make_response(jsonify({"all_keys": all_values}), 200)

if __name__ == '__main__':
    app.run()