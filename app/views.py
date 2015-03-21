from flask import Flask, render_template, json, url_for
from app import app

@app.route('/')
def hello():
	return 'my Hello World!'

@app.route('/index/')
def index():
	return render_template('base.html')
