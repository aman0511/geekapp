from flask import render_template
from app import app

@app.route('/')
def hello():
	return 'my Hello World!'

