# Fully Complete

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy import select
from website.management.database_management import database
from website.models.database_models import Employee, EmployeeAddress
from website.management.form_management import RegisterForm
from website.management.hash_management import HashManagement
from website.management.regexp_management import RegexpManagement


registration = Blueprint("registration", __name__, static_folder="./website/static", template_folder="templates")


# Need to add Email verification
@registration.route("/register", methods=["GET", "POST"])
def registration_page():

    if current_user.is_authenticated:
        return redirect(url_for("time4sport.home"))

    registration_form = RegisterForm()

    if registration_form.validate_on_submit():

        find_employee_by_email = database.session.execute(
            select(Employee).where(Employee.email_address == str(registration_form.email_address.data.lower())))

        find_employee_by_phone_number = database.session.execute(
            select(Employee).where(Employee.phone_number == str(registration_form.phone_number.data)))

        find_email = True if ([employee[0] for employee in find_employee_by_email] != []) else False
        find_phone = True if ([employee[0] for employee in find_employee_by_phone_number] != []) else False

        if find_email is True:
            flash("This email address already has an account created.", category="error")
            return redirect(url_for("registration.registration_page"))
        if RegexpManagement.check_phone_number(str(registration_form.phone_number.data)) is False:
            flash("Please enter a valid UK phone number.", category="error")
            return redirect(url_for("registration.registration_page"))
        elif find_phone is True:
            flash("This phone number is already attached to an account.", category="error")
            return redirect(url_for("registration.registration_page"))
        elif registration_form.password.data != registration_form.repeat_password.data:
            flash("You did not re enter your password correctly.", category="error")
            return redirect(url_for("registration.registration_page"))
        elif len(registration_form.password.data) < 8:
            flash("Password length must be at least 8 characters.", category="error")
            return redirect(url_for("registration.registration_page"))

        else:

            # We add type: ignore because PyCharm sees this as an unexpected argument when it is not.
            # https://stackoverflow.com/questions/58936116/pycharm-warns-about-unexpected-arguments-for-sqlalchemy-user-model

            new_employee = Employee(first_name=registration_form.first_name.data,  # type: ignore
                                    last_name=registration_form.last_name.data,  # type: ignore
                                    email_address=registration_form.email_address.data.lower(),  # type: ignore
                                    phone_number=registration_form.phone_number.data,  # type: ignore
                                    password=HashManagement.hash_password(registration_form.password.data),  # type: ignore
                                    first_aid_trained=registration_form.first_aid_trained.data)  # type: ignore

            database.session.add(new_employee)
            database.session.commit()

            new_employee_address = EmployeeAddress(employee_id=new_employee.employee_id,
                                                   address_line_one=registration_form.address_line_one.data,
                                                   address_line_two=registration_form.address_line_two.data,
                                                   address_city=registration_form.address_city.data,
                                                   address_post_code=registration_form.address_post_code.data)

            database.session.add(new_employee_address)
            database.session.commit()

            flash("Account created, please check your emails to verify account.", category="success")
            return redirect(url_for("registration.registration_page"))

    else:
        try:
            if registration_form.errors["email_address"][0] == "Invalid email address.":
                flash("Please enter a valid email address.", category="error")
                return redirect(url_for("registration.registration_page"))
        except KeyError:
            pass
        return render_template("register.html", form=registration_form)


@registration.route("/testdata", methods=["GET"])
def test_data():
    find_employee = database.session.execute(select(Employee).where(Employee.email_address == "example@outlook.com"))

    find_email = True if ([employee[0] for employee in find_employee] != []) else False

    print([employee[0] for employee in find_employee])
    print(find_email)

    return "test"
