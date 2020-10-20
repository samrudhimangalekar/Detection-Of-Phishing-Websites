import os
import phishing_detection
import blacklist
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask import jsonify
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route('/result')
def result():
    urlname  = request.args['name']
    result  = phishing_detection.getResult(urlname)
    return result

@app.route('/insert')
def insert():
    urlname  = request.args['name']
    result1  = blacklist.add(urlname)
    if result1== True:
       ok = "Added Successfully"
       return ok

@app.route('/', methods = ['GET', 'POST'])
def hello():
	return  render_template("getInput.html")

if __name__ == '__main__':
    app.run(debug=True)
