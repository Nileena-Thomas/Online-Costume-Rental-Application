
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ece1779-a2-secretkey'
    ZONE = 'Canada/Eastern'
