from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

time4sport_admin = Blueprint("time4sport_admin", __name__, static_folder="static", template_folder="templates")


@time4sport_admin.route("/", methods=["GET", "POST"])
@login_required
def admin_index():
    return "Admin Home Page"


@time4sport_admin.route("/login", methods=["GET", "POST"])
def admin_login():
    pass


@time4sport_admin.route("/home", methods=["GET", "POST"])
def admin_home():
    pass


@time4sport_admin.route("/create-school", methods=["GET", "POST"])
def create_school():
    pass


@time4sport_admin.route("/create-camp", methods=["GET", "POST"])
def create_camp():
    pass


@time4sport_admin.route("/generate-schedule", methods=["GET", "POST"])
def generate_schedule():
    pass


@time4sport_admin.route("/schedule", methods=["GET", "POST"])
def admin_schedule():
    pass


@time4sport_admin.route("/payroll", methods=["GET", "POST"])
def admin_payroll():
    pass
