from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///immersive_theater.db'
    app.config['SECRET_KEY'] = 'anykey' #switch before release   
    
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .view import api as api_blueprint
    app.register_blueprint(api_blueprint)


    return app
