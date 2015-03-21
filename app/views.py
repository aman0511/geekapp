import json
import os
from flask import render_template, request
from app import app
from models import MemberDetails, memberSession
from app import db
from flask import Flask, jsonify


@app.route('/')
def base():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/js", "data.json")
    data = json.load(open(json_url))
    for i, data in enumerate(data['data']):
        kwargs = dict()
        kwargs['id'] = str(data[0])
        kwargs['Loksabha_session'] = str(data[4])
        kwargs['total_sitting'] = str(data[7])
        kwargs['no_days_member_signed_the_register'] = str(data[8])
        member = memberSession(**kwargs)
        db.session.add(member)
        db.session.commit()
    return render_template('base.html')


@app.route('/search/page/')
def search_page():
    if 'anything' in request.form:
        data = MemberDetails.query.whoosh_search('post').un()
    elif 'name' in request.form:
        kwargs = dict()
        kwargs['name'] = 'sha'
        a = dict()
        a['name'] = 'name'
        for key, value in kwargs.iteritems():
            data = MemberDetails.query.filter(MemberDetails.a[key].like
                                              ("%"+value+"%")).all()
        print data[0].sessions.all()
    return "sucess"
