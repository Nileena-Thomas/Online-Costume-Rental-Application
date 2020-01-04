from flask import render_template, url_for, session, redirect, request
from flaskr import wapp
from flaskr import models
import traceback
import json


@wapp.route('/home_barbershop', methods=['GET', 'POST'])
def home_barbershop():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        try:
            barbershop_name = user['name']
            barbershop = models.BarberShopTable().get_barbershop(barbershop_name)
            reviews = models.ReviewTable().get_all_review()
            total = 0
            count = 0
            for review in reviews:
                if review['barbershop'] == barbershop_name:
                    total += int(review['rating'])
                    count += 1
            if count != 0:
                avg1 = round(total / count, 1)
                avg2 = total // count
            else:
                avg1 = 0
                avg2 = 0
            return render_template('home_barbershop.html', barbershop=barbershop, avg1=avg1, avg2=avg2)
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            return render_template('error.html', msg='something goes wrong~')


@wapp.route('/get_barbershop_resv', methods=['GET', 'POST'])
def get_babershop_resv():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        try:
            print('request info', request.form['bbname'])
            barbershop_name = request.form['bbname']
            resv_table = models.ResvTable()
            resvs = resv_table.get_all_reserve()
            res = []
            for resv in resvs:
                if resv['barbershop_name'] == barbershop_name and resv['customer_name'] != 'nobody':
                    fromT = int(resv['time_slot']) * 1 + 9
                    toT = fromT + 1
                    Time = str(fromT) + ":00 - " + str(toT) + ":00"
                    res.append({
                        'Time': Time,
                        'Barber': resv['barber'],
                        'Price': resv['price'],
                        'Resvid': resv['resvid'],
                        'Customer': resv['customer_name']
                    })
            # print(res)
            return json.dumps({"data": res})

        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            return None


@wapp.route('/get_barbershop_review', methods=['GET', 'POST'])
def get_barbershop_review():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        try:
            barbershop_name = request.data.decode('utf-8')
            review_table = models.ReviewTable()
            reviews = review_table.get_all_review()

            res = []
            for review in reviews:
                if review['barbershop'] == barbershop_name:
                    res.append({
                        'Customer': review['customer'],
                        'Rating': review['rating'],
                        'Text': review['text'],
                    })
            print(res)
            return json.dumps({"data": res})

        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            return None
