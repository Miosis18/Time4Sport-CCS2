from flask import Blueprint
from flask_login import login_required

time4sport = Blueprint("time4sport", __name__, static_folder="static", template_folder="templates")


@time4sport.route("/", methods=["GET", "POST"])
def index():
    return "<h1>Wow, this is the index page.</h1>"


@time4sport.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return "Wowza the home page"


@time4sport.route("/availability", methods=["GET", "POST"])
def set_availability():
    pass


@time4sport.route("/admin", methods=["GET", "POST"])
def admin():
    pass


@time4sport.route("/admin/home", methods=["GET", "POST"])
def admin_home():
    pass


@time4sport.route("/", methods=["GET", "POST"])
def schedule():
    pass


@time4sport.route("/", methods=["GET", "POST"])
def payroll():
    pass
