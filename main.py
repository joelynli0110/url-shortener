from flask import Flask, request, render_template, jsonify
# import os
# import sys
# sys.path.append('./')
from src.shorten_url import encode_url, decode_url, is_valid_url, is_valid_id
import json
import flask

app = Flask(__name__)

DOMAIN = 'http://127.0.0.1:5000/' # the default domain of short url

def generate_short_url(short_id):
    return DOMAIN+short_id

@app.route("/to-short-url", methods=['POST'])
def to_short_url():
    original_url = request.form["original_url"]
    # check if the given url is valid
    if not is_valid_url(original_url):
        response = jsonify({'error message': 'The given url is invalid!'})
        response.status_code = 400
        return response

    print(original_url)
    short_id = encode_url(original_url,1) # Generate unique id of short url
    data_dic = {
        "full": original_url,
        "short": generate_short_url(short_id)
    }
    result_json = flask.json.htmlsafe_dumps(data_dic)
    return jsonify(result_json),201

@app.route("/to-original-url", methods=['POST'])
def to_original_url():
    short_url = request.form["short_url"]
    short_id = short_url.split('/')[-1]

    # check if the given id is valid
    if not is_valid_id(short_id):
        response = jsonify({'error message': 'The given short id is invalid!'})
        response.status_code = 400
        return response

    original_url = decode_url(short_id)
    data_dic = {
        "short": short_url,
        "full": original_url
    }
    result_json = json.dumps(data_dic)
    return jsonify(result_json),201

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()