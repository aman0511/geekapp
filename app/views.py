import json
import os
from flask import render_template, request
from app import app
from models import MemberDetails, memberSession
from app import db
from flask import Flask, jsonify


@app.route('/datainsert/')
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


@app.route('/search/page/', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        if request.form['parameter'] == "all":
            datas = MemberDetails.query.whoosh_search('soni').all()
        elif request.form['parameter'] == "state":
            datas = MemberDetails.query.filter(MemberDetails.state.like
                                               (request.form['value']+"%")
                                               ).all()
        elif request.form['parameter'] == "name":
            datas = MemberDetails.query.filter(MemberDetails.name.like
                                               ("%"+request.form['value']+"%")
                                               ).all()
        elif request.form['parameter'] == "constituency":
            datas = MemberDetails.query.filter(MemberDetails.constituency.like
                                               ("%"+request.form['value']+"%")
                                               ).all()
        else:
            datas = []
        att_avg = dict()
        for data in datas:
            attendnace_avg(data)
        template_data = {}
        template_data['html'] = render_template('name.html', datas=datas)
        template_data['avg'] = att_avg
        return jsonify(template_data)


        #     output = []
        #     for data in datas:
        #         row = {}
        #         print MemberDetails.__table__.c
        #         for column in MemberDetails.__table__.columns:
        #             row[str(column.name)] = getattr(data, str(column.name))
        #         output.append(row)
        # return jsonify(result=output)


@app.route('/index/')
def index():
    return render_template('base.html')


@app.route('/list/', methods=['GET', 'POST'])
def auto_listing():
    if request.method == 'POST':
        if request.form['parameter'] == "all":
            datas = MemberDetails.query.whoosh_search('soni').all()
        elif request.form['parameter'] == "state":
            datas = MemberDetails.query.with_entities(MemberDetails.state.distinct()).all()
        elif request.form['parameter'] == "name":
            datas = MemberDetails.query.with_entities(MemberDetails.name.distinct()).all()
        elif request.form['parameter'] == "constituency":
            datas = MemberDetails.query.with_entities(MemberDetails.constituency.distinct()).all()
        else:
            datas = []
        tags = []
        for data in datas:
            tags.append(data[0].rstrip())
        # for data in datas:
        #     row = {}
        #     print MemberDetails.__table__.c
        #     for column in MemberDetails.__table__.columns:
        #         row[str(column.name)] = getattr(data, str(column.name))
        #     output.append(row)
        return jsonify(result=tags)


def attendnace_avg(data):
    total_attend = 0
    total = 0
    for attend in data.sessions:
        try:
            print attend.no_days_member_signed_the_register
            total_attend += int(attend.no_days_member_signed_the_register)
            print "hello"+total_attend
        except:
            total_attend += 0
        try:
            total += int(attend.total_sitting)
        except:
            total += 0
        attend.session_avg = str(round((int(attend.no_days_member_signed_the_register)/float(attend.total_sitting))*100,2))
        db.session.merge(attend)
        db.session.commit()
    data.total_avg = str(round((float(total_attend) / total)*100, 2))
    db.session.merge(data)
    db.session.commit()

@app.route('/person/<id>',methods=['GET','POST'])
def person(id):
	member = MemberDetails.get_member(int(id))
	print member.sessions
	template_data = dict()
	template_data['html'] = render_template('table.html',person=member)
	return jsonify(template_data)