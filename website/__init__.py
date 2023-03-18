from flask import Flask
from flask_login import LoginManager
from website.views.registration_page import registration
from website.views.login_page import login
from website.views.time4sport import time4sport
from website.views.time4sport_admin import time4sport_admin
from website.management.dummy_data import fakedata
from website.models.database_models import Employee
from website.management.database_management import database


def create_app():
    app = Flask(__name__, static_folder="../website/static")
    app.register_blueprint(registration, url_prefix="")
    app.register_blueprint(login, url_prefix="")
    app.register_blueprint(time4sport, url_prefix="")
    app.register_blueprint(time4sport_admin, url_prefix="/admin")
    app.register_blueprint(fakedata, url_prefix="")

    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "KeepThisASecret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@127.0.0.1:3306/time4sport"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    database.init_app(app)
    app.app_context().push()
    database.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "login.login_page"
    login_manager.login_message_category = "error"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.get(int(user_id))

    return app
