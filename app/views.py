from flask import render_template
from app import app


@app.route('/')
def base():
    with open('data.json') as json_data:
    d = json.loads(json_data)
    print d
    return render_template('base.html')
