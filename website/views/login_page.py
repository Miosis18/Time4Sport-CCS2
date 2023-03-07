from flask import Blueprint, url_for, redirect, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select
from website.management.database_management import database
from website.models.database_models import Employee
from website.management.form_management import LoginForm
from website.management.hash_management import HashManagement


login = Blueprint("login", __name__, static_folder="static", template_folder="templates")


@login.route("/login", methods=["GET", "POST"])
def login_page():

    if current_user.is_authenticated:
        return redirect(url_for("time4sport.home"))

    login_form = LoginForm()

    if login_form.validate_on_submit():

        find_employee_by_email = database.session.execute(
            select(Employee).where(Employee.email_address == str(login_form.email_address.data.lower())))

        employee_object = [employee[0] for employee in find_employee_by_email]
        find_email = True if (employee_object != []) else False

        if ((find_email is True) and (
                HashManagement.verify_password(employee_object[0].password, login_form.password.data))):
            # No need for a flash message as they will never see it, they will be redirected to the home page.
            login_user(employee_object[0], remember=True)
            return redirect(url_for("time4sport.home"))
        else:
            flash("Sorry the credentials entered were not correct.", category="error")
            return redirect(url_for("login.login_page"))
    else:
        try:
            if login_form.errors["email_address"][0] == "Invalid email address.":
                flash("Sorry the credentials entered were not correct.", category="error")
                return redirect(url_for("login.login_page"))
        except KeyError:
            pass
        return render_template("login.html", form=login_form)


@login.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.login_page"))


# Needs completing
@login.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("time4sport.home"))

    return "Oh no lets reset your password"
