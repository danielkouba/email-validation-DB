from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
mysql = MySQLConnector(app, 'emails')

app.secret_key  = "BeholdThePowerOfGreySkull"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



@app.route('/')
def index():
	return render_template('index.html')

@app.route('/process', methods=(['POST']))
def process_form():

	if len(request.form['email']) < 1:
		flash( "WHOOPS! Email cannot be empty",'email')
		return redirect('/')
	elif not EMAIL_REGEX.match(request.form['email']):
		flash( "WHOOPS! Email address is not valid",'email')
		return redirect('/')
	else:
		flash( "Success! you successfully registered {}".format(request.form['email']),'success')
		session['email'] = request.form['email']
		query = "INSERT INTO emails (email, created_at, updated_at) VALUES ( :email , NOW(), NOW())"
		data = {
			"email" : session['email']
		}
		mysql.query_db(query, data)
		return redirect('/success')

@app.route('/success')
def success():
	query = "SELECT * FROM emails ORDER BY id DESC"
	emails = mysql.query_db(query)
	return render_template('success.html', all_emails = emails)

@app.route('/remove/<email_id>')
def delete(email_id):
    query = "DELETE FROM emails WHERE id = :id"
    data = {'id': email_id}
    mysql.query_db(query, data)
    return redirect('/success')

app.run(debug=True)