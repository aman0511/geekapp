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
        # kwargs['name'] = str(data[2])
        # kwargs['division_or_seat_no'] = str(data[1])
        # kwargs['Loksabha'] = str(data[3])
        # kwargs['state'] = str(data[5])
        # kwargs['constituency'] = str(data[6])
        # member = MemberDetails(**kwargs)
        kwargs['id'] = str(data[0])
        kwargs['Loksabha_session'] = str(data[4])
        kwargs['total_sitting'] = str(data[7])
        kwargs['no_days_member_signed_the_register'] = str(data[8])
        try:
            total = int(data[7])
        except:
            total = 0
        try:
            total_sitting = int(data[8])
        except:
            total_sitting = 0
        try:
            avg = (float(total_sitting)/total)*100
        except:
            avg = 0

        kwargs['session_avg'] = str(round(avg, 2))
        member = memberSession(**kwargs)
        db.session.add(member)
        db.session.commit()
        member = MemberDetails.get_member(int(kwargs['id']))
        total_sitting = 0
        total = 0
        for sess in member.sessions:
            try:
                total += int(sess.total_sitting)
            except:
                total += 0
            try:
                total_sitting += int(sess.no_days_member_signed_the_register)
            except:
                total_sitting += 0
            percentage = (float(total_sitting)/total)*100
            member.total_avg = percentage
            db.session.merge(member)
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
        template_data = {}
        template_data['html'] = render_template('name.html', datas=datas)
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


@app.route('/person/<id>',methods=['GET','POST'])
def person(id):
	member = MemberDetails.get_member(int(id))
	datas = MemberDetails.query.with_entities(MemberDetails.name.distinct()).all()
	graphdata = dict()
	for sessions in member.sessions:
		graphdata[sessions.Loksabha_session]=sessions.no_days_member_signed_the_register
	print graphdata
	return render_template('person.html',person=member,graphdata=graphdata)

