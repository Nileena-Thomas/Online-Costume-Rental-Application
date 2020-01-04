from flask import render_template, url_for, session, redirect, request
from flaskr import wapp
from flaskr import models
import traceback
import json

@wapp.route('/barbershop', methods=['GET', 'POST'])
def barbershop():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        try:
            barbershop_name = request.values['name']
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
            return render_template('barbershop.html', barbershop=barbershop, avg1=avg1, avg2=avg2)
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            return render_template('error.html', msg='something goes wrong~')

@wapp.route('/get_resv', methods=['GET', 'POST'])
def get_resv():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        try:
            barbershop_name = request.form['bbname']
            #barbershop_name = '9dAD-8EqSCO3nVPiiOKKDg=='
            resv_table = models.ResvTable()
            resvs = resv_table.get_all_reserve()
            res = []
            for resv in resvs:
                if resv['barbershop_name'] == barbershop_name and resv['customer_name'] == 'nobody':
                    fromT = int(resv['time_slot']) * 1 + 9
                    toT = fromT + 1
                    Time = str(fromT) + ":00 - " + str(toT) + ":00"
                    res.append({
                        'Time': Time,
                        'Barber': resv['barber'],
                        'Price': resv['price'],
                        'Resvid': resv['resvid']
                    })
            print("resssss",res)
            return json.dumps({"data": res})
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            return None

@wapp.route('/put_resv', methods=['GET', 'POST'])
def put_resv():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        try:
            print(request.data.decode('utf-8'))
            resvid = request.data.decode('utf-8')
            resv_table = models.ResvTable()
            resv = resv_table.get_reserve(resvid)
            print(resv)
            print(user['name'])
            print(resv['customer_name'])
            resv['customer_name'] = user['name']
            print(resv)
            resv_table.put_reserve_new(resv)
            print('heheheh')
            return "1"
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            return "0"

@wapp.route('/get_history', methods=['GET', 'POST'])
def get_history():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        try:
            resv_table = models.ResvTable()
            resvs = resv_table.get_all_reserve()
            res = []
            for resv in resvs:
                print('print customer name and user_name',resv['customer_name'], user['name'])
                if resv['customer_name'] == user['name']:
                    fromT = int(resv['time_slot']) * 1 + 9
                    toT = fromT + 1
                    Time = str(fromT) + ":00 - " + str(toT) + ":00"
                    res.append({
                        'Time': Time,
                        'Barber': resv['barber'],
                        'Price': resv['price'],
                        'Resvid': resv['resvid'],
                        'Barbershop': resv['barbershop_title']
                    })
            print('print res results',res)
            return json.dumps({"data": res})
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            return None
@wapp.route('/history', methods=['GET', 'POST'])
def history():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        return render_template('history.html')

@wapp.route('/get_review', methods=['GET', 'POST'])
def get_review():
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

@wapp.route('/put_review', methods=['GET', 'POST'])
def put_review():
    user = session['user'] if 'user' in session else None
    if not user:
        return redirect(url_for('login'))
    else:
        try:
            ret = json.loads(request.data.decode('utf-8'))
            print(ret)
            review_table = models.ReviewTable()
            review_table.put_review(user['name'], ret['barbershop'], ret['text'], ret['rating'])
            return "1"
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            return "0"