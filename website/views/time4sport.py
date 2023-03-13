from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

time4sport = Blueprint("time4sport", __name__, static_folder="static", template_folder="templates")


@time4sport.route("/", methods=["GET", "POST"])
@login_required
def index():
    return redirect(url_for("login.login_page"))


@time4sport.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", name=current_user.first_name)


@time4sport.route("/availability", methods=["GET", "POST"])
def set_availability():
    pass


@time4sport.route("/schedule", methods=["GET", "POST"])
def schedule():
    pass


@time4sport.route("/payroll", methods=["GET", "POST"])
def payroll():
    pass


# Admin Pages

@time4sport.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    pass


@time4sport.route("/admin/home", methods=["GET", "POST"])
def admin_home():
    pass


@time4sport.route("/admin/create-school", methods=["GET", "POST"])
def create_school():
    pass


@time4sport.route("/admin/create-camp", methods=["GET", "POST"])
def create_camp():
    pass


@time4sport.route("/admin/generate-schedule", methods=["GET", "POST"])
def generate_schedule():
    pass


@time4sport.route("/admin/schedule", methods=["GET", "POST"])
def admin_schedule():
    pass


@time4sport.route("/admin/payroll", methods=["GET", "POST"])
def admin_payroll():
    pass
