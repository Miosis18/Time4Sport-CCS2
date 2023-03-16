from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from website.management.form_management import EmployeeAvailabilityForm

time4sport = Blueprint("time4sport", __name__, static_folder="static", template_folder="templates")


@time4sport.route("/", methods=["GET", "POST"])
@login_required
def index():
    return redirect(url_for("time4sport.home"))


@time4sport.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", name=current_user.first_name)


@time4sport.route("/availability", methods=["GET", "POST"])
def set_availability():
    form = EmployeeAvailabilityForm()
    if form.validate_on_submit():
        # Handle form submission
        pass
    return render_template('set-availability.html', form=form)


@time4sport.route("/schedule", methods=["GET", "POST"])
def schedule():
    pass


@time4sport.route("/payslips", methods=["GET", "POST"])
def payroll():
    pass


@time4sport.route("/upload-documents", methods=["GET", "POST"])
def upload_documents():
    pass
