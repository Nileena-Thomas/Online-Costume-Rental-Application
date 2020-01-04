from flask import Flask
from flaskr.config import Config
import boto3

wapp = Flask(__name__)
wapp.config.from_object(Config)

from flaskr import home
from flaskr import home_barbershop
from flaskr import tryout
from flaskr import barbershop
from flaskr import login
from flaskr import error
