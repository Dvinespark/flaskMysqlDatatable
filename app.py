import json

from flask import Flask, request, render_template, url_for, jsonify
from werkzeug.utils import secure_filename
import datetime
import os
import pymysql

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1234'
DATABASE = 'testdb'

app = Flask(__name__, static_url_path='/static')

# Mysql Configuration


db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DATABASE)


@app.route('/')
def index():
    sql = 'SELECT * FROM applicants;'
    with db.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    context = {
        'data': json.dumps(results)
    }
    print(context['data'])
    return render_template("index.html", context=context)


@app.route('/filter')
def filter():
    skills = request.args.get('skills', '')
    years = request.args.get('years', '')
    lastname = request.args.get('lastname', '')
    print(request)
    query = "SELECT * FROM applicants WHERE lower(skill) like '%{0}%' and years like '%{1}%' and " \
            "lower(lastname) like '%{2}%'; ".format(skills.lower() if skills else '',
                                                    years if years else '', lastname.lower() if lastname else '')
    print(query)
    with db.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return {
        "status_code": 200,
        "message": "data fetched successfully.",
        "data": json.dumps(results)
    }


@app.route('/create', methods=['post'])
def user_create():
    print("method called")
    print(request.form)
    print(request.files)

    data = {
        "firstname": request.form.get('firstname', None),
        "lastname": request.form.get('lastname', None),
        "email": request.form.get('email', None),
        "phone": request.form.get('phone_number', None),
        "skill1": request.form.get("skill1", None),
        "nskill1": request.form.get("nskill1", None),
        "skill2": request.form.get("skill2", None),
        "nskill2": request.form.get("nskill2", None),
        "skill3": request.form.get("skill3", None),
        "nskill3": request.form.get("nskill3", None),
        "status": request.form.get("status", None),
        "availability": request.form.get("availability", None),
    }
    if 'resume' in request.files:
        file = request.files['resume']
        import flask
        file_name = secure_filename(file.filename)
        file_name = file_name.split('.')[0].strip() + "_" + str(datetime.date.today()) + \
                    "." + file_name.split('.')[1]
        file.filename = file_name
        file_path = os.path.join(flask.current_app.root_path, 'static', 'files', file_name)
        file.save(file_path)

        data['resume'] = file_name

    query = """
    INSERT INTO applicants (firstname, lastname, email, phone, status, availability, skill, years, resume) VALUES 
"""
    if data['skill1'] is not None:
        query = query + "('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}')". \
            format(data['firstname'], data['lastname'], data['email'], data['phone'], data['status'],
                   data['availability'], data['skill1'], data['nskill1'], data['resume'])

    if data['skill2'] is not None:
        query = query + " , "
        query = query + "('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}')". \
            format(data['firstname'], data['lastname'], data['email'], data['phone'], data['status'],
                   data['availability'], data['skill2'], data['nskill2'], data['resume'])

    if data['skill3'] is not None:
        query = query + " , "
        query = query + "('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7}, '{8}')". \
            format(data['firstname'], data['lastname'], data['email'], data['phone'], data['status'],
                   data['availability'], data['skill3'], data['nskill3'], data['resume'])

    query = query + ";"
    print(query)

    with db.cursor() as cursor:
        cursor.execute(query)
        db.commit()
    return {
        "status_code": 200,
        "message": "user created successfully.",
        "url": url_for('index')
    }


if __name__ == '__main__':
    app.run()
