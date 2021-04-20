from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
#from flask_wtf import CsrfProtect

db = SQLAlchemy()
DB_NAME = "DB_SmartParking.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '\x1a\x96\x8b\xd3\x8e\xb6\n\x0e\xb4\xa6\xf6\x1d'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #csrf = CsrfProtect()

    db.init_app(app)
    #csrf.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Parking
    from .models import Arrival

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
