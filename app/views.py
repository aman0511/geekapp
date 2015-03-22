import json
import os
from flask import render_template, request, g, url_for, redirect
from app import app, lm
from models import MemberDetails, memberSession, User
from app import db
from flask import Flask, jsonify
from flask.ext.login import login_user, current_user, logout_user, \
                     login_required
from oauth import OAuthSignIn

@lm.user_loader
def load_user(id):
    return User.query.get(id)


@app.before_request
def before_request():
    g.user = current_user


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
    return "404"


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


@app.route('/no_of_analaysis/')
def data_analaysis():
    sessions = db.session.query(memberSession.Loksabha_session.distinct()).all()
    kwargs = dict()
    for sessions in sessions:
        kwargs[sessions.Loksabha_session] = sessions.Loksabha_session
    print kwargs
    return "sucees"


@app.route('/authorize/<provider>', methods=['GET', 'POST'])
def oauth_authorize(provider=None):
    if not g.user.is_anonymous():
        return redirect(url_for('index'))
    else:
        oauth = OAuthSignIn.get_provider(provider)
        return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not g.user.is_anonymous():
        return redirect(url_for('home'))
    oauth = OAuthSignIn.get_provider(provider)
    me = oauth.callback()
    kwargs = dict()
    kwargs['email'] = me['email']
    kwargs['social_id'] = me['id']
    kwargs['name'] = me['name']
    user = User.authenticate_user(**kwargs)
    if user:
        login_user(user)
        return redirect(url_for('index'))
    else:
        try:
            user = User(**kwargs)
            login_user(user, True)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print e
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    ''' logout view '''
    logout_user()
    return redirect(url_for('index'))


@app.route('/person/<id>',methods=['GET','POST'])
def person(id):
	member = MemberDetails.get_member(int(id))
	datas = MemberDetails.query.with_entities(MemberDetails.name.distinct()).all()
	graphdata = dict()
	for sessions in member.sessions:
		graphdata[sessions.Loksabha_session]=sessions.no_days_member_signed_the_register
	print graphdata
	return render_template('person.html',person=member,graphdata=graphdata)


