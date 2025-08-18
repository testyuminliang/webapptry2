# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Lxygwqf0725!@localhost:3306/my_flask_app_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False