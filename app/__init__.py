# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from config import Config
from .models import db
from .api.users import users_api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化插件
    db.init_app(app)
    Migrate(app, db)

    # 注册蓝图
    # url_prefix='/api' 的意思是，这个蓝图里所有的路由都会自动加上 /api 前缀
    # 所以 /users 会变成 /api/users
    app.register_blueprint(users_api_bp, url_prefix='/api')

    return app