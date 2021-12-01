from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_user import UserManager, current_user

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Flask-Mail SMTP server settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = 'jeff.gilbert.codes@gmail.com'
    app.config['MAIL_PASSWORD'] = 'LumpkinGt450'
    app.config['MAIL_DEFAULT_SENDER'] = '"MyApp" <noreply@example.com>'

    # Flask-User settings
    app.config['USER_APP_NAME'] = "Pick and Bow CRM"      # Shown in and email templates and page footers
    app.config['USER_ENABLE_EMAIL'] = True        # Enable email authentication
    app.config['USER_ENABLE_USERNAME'] = False    # Disable username authentication
    app.config['USER_EMAIL_SENDER_NAME'] = app.config['USER_APP_NAME']
    app.config['USER_EMAIL_SENDER_EMAIL'] = "noreply@example.com"


    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Role, UserRoles

    user_manager = UserManager(app, db, User)

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
