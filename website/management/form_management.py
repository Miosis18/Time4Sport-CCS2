from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Optional

from datetime import date, timedelta
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    first_name = StringField("First Name*", validators=[InputRequired()])
    last_name = StringField("Last Name*", validators=[InputRequired()])
    email_address = StringField("Email Address*", validators=[InputRequired(), Email()])
    phone_number = StringField("Phone Number", validators=[Optional()])
    password = PasswordField("Password*", validators=[InputRequired()])
    repeat_password = PasswordField("Repeat Password*", validators=[InputRequired()])
    address_line_one = StringField("Address Line One*", validators=[InputRequired()])
    address_line_two = StringField("Address Line Two", validators=[Optional()])
    address_city = StringField("Address City*", validators=[InputRequired()])
    address_post_code = StringField("Address Post Code*", validators=[InputRequired()])
    first_aid_trained = BooleanField("Are you first aid trained?*", validators=[Optional()])


class LoginForm(FlaskForm):
    email_address = StringField("Email Address*", validators=[InputRequired(), Email()])
    password = PasswordField("Password*", validators=[InputRequired()])


class ForgotPasswordForm(FlaskForm):
    email_address = StringField("Email Address*", validators=[InputRequired(), Email()])


class EmployeeAvailabilityForm(FlaskForm):
    pass


class SchoolCreationForm(FlaskForm):
    pass


class CampCreationForm(FlaskForm):
    pass
