import os
from models import *
import aws
import base64
import uuid
import re
from random import randint
import json
from datetime import datetime

def get_rand_lat_lon():
    min_lat, max_lat = 436416, 437977
    min_lon, max_lon = -796012, -793229
    lat = randint(min_lat, max_lat)
    lon = randint(min_lon, max_lon)
    return str(lat), str(lon)

def get_rand_barbers():
    candidates = ['Ironman', 'Superman', 'Supergirl', 'Wonderwomen', 'Thor', 'Dr.Strange', 'Spiderman',
                  'Batman', 'Antman', 'Joker', 'Nun', 'Yoda', 'Princess Leia', 'Elsa', 'Captain America']

    n = len(candidates)
    a = candidates[randint(0, n-1)]
    b = candidates[randint(0, n-1)]
    return a, b

def get_rand_cust():
    candidates = ['Jacky', 'Johny', 'Amyy', 'Samy', 'Olivery', 'Harryy', 'Jacoby', 'Charliey',
                  'Thomasy', 'Georgey', 'Oscary', 'Jamesy', 'Williamy', 'Noahy', 'Liamy',
                  'Masony', 'Jacoby', 'Williamy', 'Ethany', 'Michaely', 'Alexandery', 'Jamesy', 'Daniely']

    n = len(candidates)
    a = candidates[randint(0, n-1)]
    b = candidates[randint(0, n-1)]



def get_rand_prices():
    min_price = 10
    max_price = 200
    return str(randint(min_price, max_price)) + '$'

def load_barbershop(dirname):
    for filename in os.listdir(dirname):
        name = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8')
        password = name
        title = re.sub('_', ' ', filename).split('.')[0]
        image = aws.upload_file(dirname, filename)
        lat, lon = get_rand_lat_lon()

        barbershop_table = BarberShopTable()
        barbershop_table.put_barbershop(name, password, title, image, lat, lon)


def load_resv():
    barbershop_table = BarberShopTable()
    barbershops = barbershop_table.get_all_barbershop()
    resv_table = ResvTable()
    count=0
    for barbershop in barbershops:
        a, b = get_rand_barbers()
        resv_table.put_reserve(barbershop['name'], a, count, get_rand_prices(), 'nobody', barbershop['title'])
        count +=1
        # print(barbershop['name'], a, 0, get_rand_prices(), 'nobody', barbershop['title'])
        # for i in range(8):
        #     print(barbershop['name'], a, str(i), get_rand_prices(), 'nobody', barbershop['title'])
            # resv_table.put_reserve(barbershop['name'], a, str(i), get_rand_prices(), 'nobody', barbershop['title'])

if __name__ == '__main__':
    dirname = r'C:\Users\harik\Desktop\photos'
    load_barbershop(dirname)
    load_resv()
    # aws.clear_s3()