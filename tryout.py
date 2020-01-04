from flask import render_template, url_for, session, redirect
from flaskr import wapp
from flaskr import models
import traceback
import json


@wapp.route('/tryout')
def tryout():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        return render_template('tryout.html')
#        "role_arn": "arn:aws:iam::011559063667:role/hairstyling-app-dev-ZappaLambdaExecutionRole",