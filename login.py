from flask import render_template, request, flash, redirect, url_for, session
from flaskr import wapp
from flaskr import forms
from flaskr.models import *
import hashlib
import base64
import uuid
import traceback


def hash_password(salt, password):
    t_sha = hashlib.sha512()
    t_sha.update(str(password + salt).encode('utf-8'))
    return base64.urlsafe_b64encode(t_sha.digest())


@wapp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if 'user' in session:
            logout()

        form = forms.LoginForm()
        if form.validate_on_submit():
            valid = True
            message = ''
            username = form.username.data
            password = form.password.data
            usertype = form.usertype.data

            if usertype == '0':  # customer
                customer_table = CustomerTable()
                user = customer_table.get_customer(username)
            else:
                barbershop_table = BarberShopTable()
                user = barbershop_table.get_barbershop(username)
                print("user ",user)

            if not user:
                valid = False
                message = "name or password does not exist"
            elif usertype == '0':
                salt = user['salt']
                password_hash = hash_password(salt, password)
                if password_hash != user['password']:
                    valid = False
                    message = "name or password does not exist"
            else:
                if user['password'] != username:
                    print("dvf",user[password])
                    valid = False
                    message = "name or password does not exist"

            if valid:
                session['user'] = {
                    'name': user['name'],
                    'usertype': usertype,
                    'title': user['title'] if 'title' in user else None
                }

                if usertype == '0':
                    return redirect(url_for('home'))
                else:
                    # obtain information
                    return redirect(url_for('home_barbershop'))
            else:
                flash(message)

        return render_template('login.html', form=form)

    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return render_template('error.html', msg='something goes wrong~')


@wapp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@wapp.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if 'user' in session:
            logout()
            return redirect(url_for('home'))

        form = forms.RegisterForm()
        if form.validate_on_submit():
            valid = True
            username = form.username.data
            password1 = form.password1.data
            customer_table = CustomerTable()
            user = customer_table.get_customer(username)
            if user:
                valid = False
                message = 'name has already existed'
            else:
                salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
                salt = salt.decode('utf-8')
                password_hash = hash_password(salt, password1)
                customer_table.put_customer(username, salt, password_hash, '0')
                message = "Sign up successfully!"
            if valid:
                flash(message, "success")
            else:
                flash(message, "danger")

        return render_template('register.html', form=form)

    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return render_template('error.html', msg='something goes wrong~')