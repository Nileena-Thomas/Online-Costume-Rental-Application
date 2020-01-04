from flask import render_template, url_for, session, redirect
from flaskr import wapp
from flaskr import models
from flaskr.recmd.predict import *
import traceback
import json

@wapp.route('/')
@wapp.route('/home')
def home():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        try:
            customer_name=[]
            customer_name = session['user']['name']
            barbershop_name_list = get_recmd_list(customer_name)
            barbershop_table = models.BarberShopTable()
            barbershop_list = []
            flag = True
            for barbershop_name in barbershop_name_list:
                res = barbershop_table.get_barbershop(barbershop_name)
                if not res:
                    flag = False
                    break
                barbershop_list.append(barbershop_table.get_barbershop(barbershop_name))
            print("barber shop lst",barbershop_list)


            if not flag:
                barbershop_list = [
                    {
                        "name": '9l49YhGNTw6V93X0Sismkg==',
                        "title": 'Hagen_Hair_And_Barber',
                        "image": 'https://s3.amazonaws.com/ece1779-images/Hagen_Hair_And_Barber.png'
                    },
                    {
                        "name": 'HekSa7uaRnqVOPm0VdGhNQ==',
                        "title": 'N15_Hair_Salon',
                        "image": 'https://s3.amazonaws.com/ece1779-images/N15_Hair_Salon.png'
                    },
                    {
                        "name": "iiZ-MKZOTECxziKXyY-naQ==",
                        "title": 'Crows_Nest_Barbershop',
                        "image": 'https://s3.amazonaws.com/ece1779-images/Crows_Nest_Barbershop.png'
                    }
                ]

            return render_template('home.html', barbershop_list=barbershop_list)

        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            return render_template('error.html', msg='something goes wrong~')


@wapp.route('/load_markers', methods=['GET', 'POST'])
def load_markers():
    barbershop_table = models.BarberShopTable()
    barbershops = barbershop_table.get_all_barbershop()
    # print(barbershops)
    return json.dumps(barbershops)

