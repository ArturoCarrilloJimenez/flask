import os

SECRET_KEY = os.urandom(32) # Genera una clave de 32 bit
PWD = os.path.abspath(os.curdir)
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/dbase.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False