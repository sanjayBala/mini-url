import json
from flask import Flask, render_template, request, jsonify, redirect, make_response, url_for, flash
from forms.forms import MainForm
from main.parser import URLShortener

# init flask app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

shortner = URLShortener()
base_url = "https://sanjay-mini-url.herokuapp.com/"
protocol_prefix="https://"

@app.route('/', methods=['POST', 'GET'])
def home():
    form = MainForm()
    # if form is submitted and validated
    if form.validate_on_submit():
        original_url = str(form.original_url.data)
        print("Processing: " + original_url)
        shortened_url, expiry_time = shortner.processUrl(original_url)
        print("Shortened URL: " + str(shortened_url))
        print("Complete.")
        if expiry_time == -1:
            expiry_time = "bazillion"
        return render_template('result.html', original_url=original_url, shortened_url=base_url+shortened_url, expiry_time=expiry_time)
    # if form is invalid
    elif form.is_submitted():
        print("Invalid form inputs")
        flash(f'Invalid URL entered!', 'warning')
    # if this is just a hit to home
    return render_template('index.html', form=form)

@app.route('/<string:shortened_url>', methods=['GET'])
def redirect_to_original(shortened_url):
    print("Processing...")
    original_url = shortner.redirectUrl(shortened_url)
    if original_url == None:
        print("Looks like this is an invalid short URL...")
        return redirect(url_for('error_page', error_message="Invalid Short URL, this Mapping is not present in our Database!"))
    original_url = str(original_url)
    print("Original URL: " + original_url)
    if protocol_prefix in original_url:
        return redirect(original_url)
    else:
        print("Appending protocol prefix... Redirecting...")
        return redirect(protocol_prefix + original_url)

@app.route('/errorhandler', methods=['GET'])
def error_page(error_message="Something went wrong"):
    return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run()