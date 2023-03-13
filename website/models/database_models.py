from flask_login import UserMixin
from website.management.database_management import database


class Employee(database.Model, UserMixin):
    __tablename__ = "employees"

    employee_id = database.Column(database.Integer, primary_key=True)
    first_name = database.Column(database.String(50), nullable=False)
    last_name = database.Column(database.String(80), nullable=False)
    email_address = database.Column(database.String(192), nullable=False, unique=True)
    phone_number = database.Column(database.String(192), unique=True)
    first_aid_trained = database.Column(database.Boolean, nullable=False, default=False)
    password = database.Column(database.String(192), nullable=False)

    address = database.relationship("EmployeeAddress", backref="employee")
    availability = database.relationship("EmployeeAvailability", backref="employee")

    def get_id(self):
        return self.employee_id


class EmployeeAddress(database.Model):
    __tablename__ = "employee_addresses"

    address_id = database.Column(database.Integer, primary_key=True)
    employee_id = database.Column(database.Integer, database.ForeignKey("employees.employee_id"), nullable=False)
    address_line_one = database.Column(database.String(80), nullable=False)
    address_line_two = database.Column(database.String(80))
    address_city = database.Column(database.String(80), nullable=False)
    address_post_code = database.Column(database.String(80), nullable=False)


class EmployeeAvailability(database.Model):
    __tablename__ = "employee_availability"
    __table_args__ = (database.UniqueConstraint('employee_id', 'week_beginning', name='one_availability_per_employee'),)

    availability_id = database.Column(database.Integer, primary_key=True)
    employee_id = database.Column(database.Integer, database.ForeignKey("employees.employee_id"), nullable=False)
    week_beginning = database.Column(database.Date, nullable=False, default=False)
    monday = database.Column(database.Boolean, nullable=False, default=False)
    tuesday = database.Column(database.Boolean, nullable=False, default=False)
    wednesday = database.Column(database.Boolean, nullable=False, default=False)
    thursday = database.Column(database.Boolean, nullable=False, default=False)
    friday = database.Column(database.Boolean, nullable=False, default=False)
    saturday = database.Column(database.Boolean, nullable=False, default=False)
    sunday = database.Column(database.Boolean, nullable=False, default=False)


class School(database.Model):
    __tablename__ = "schools"

    school_id = database.Column(database.Integer, primary_key=True)
    school_name = database.Column(database.String(128), nullable=False)
    total_students = database.Column(database.Integer, nullable=False)


class SchoolAddress(database.Model):
    __tablename__ = "school_addresses"

    address_id = database.Column(database.Integer, primary_key=True)
    school_id = database.Column(database.Integer, database.ForeignKey("schools.school_id"), nullable=False)
    address_line_one = database.Column(database.String(80), nullable=False)
    address_line_two = database.Column(database.String(80))
    address_line_three = database.Column(database.String(80))
    address_city = database.Column(database.String(80), nullable=False)
    address_post_code = database.Column(database.String(80), nullable=False)


# Camps require three employees per day
class Camp(database.Model):
    __tablename__ = "camps"

    camp_id = database.Column(database.Integer, primary_key=True)
    school_id = database.Column(database.Integer, database.ForeignKey("schools.school_id"), nullable=False)
    camp_start_time = database.Column(database.DateTime)
    camp_finishing_time = database.Column(database.DateTime)

    availability_requirements = database.relationship("CampAvailabilityRequirements", backref="camp")


class CampAvailabilityRequirements(database.Model):
    __tablename__ = "camp_availability_requirements"
    __table_args__ = (database.UniqueConstraint('camp_id', 'week_beginning', name='one_availability_per_camp'),)

    availability_id = database.Column(database.Integer, primary_key=True)
    camp_id = database.Column(database.Integer, database.ForeignKey("camps.camp_id"), nullable=False)
    week_beginning = database.Column(database.Date, nullable=False, default=False)
    monday = database.Column(database.Boolean, nullable=False, default=False)
    tuesday = database.Column(database.Boolean, nullable=False, default=False)
    wednesday = database.Column(database.Boolean, nullable=False, default=False)
    thursday = database.Column(database.Boolean, nullable=False, default=False)
    friday = database.Column(database.Boolean, nullable=False, default=False)
    saturday = database.Column(database.Boolean, nullable=False, default=False)
    sunday = database.Column(database.Boolean, nullable=False, default=False)


# One schedule per employee per day (Camps will require three schedule entries each)
class Schedule(database.Model):
    __tablename__ = "schedules"
    __table_args__ = (database.UniqueConstraint('employee_id', 'camp_id', 'week_beginning', 'scheduled_day'),)

    schedule_id = database.Column(database.Integer, primary_key=True)
    employee_id = database.Column(database.Integer, database.ForeignKey("employees.employee_id"), nullable=False)
    camp_id = database.Column(database.Integer, database.ForeignKey("camps.camp_id"), nullable=False)
    week_beginning = database.Column(database.Date, nullable=False)
    scheduled_day = database.Column(database.String(9), nullable=False)


class ShortDays(database.Model):
    __tablename__ = 'short_days'
    __table_args__ = (database.UniqueConstraint('camp_id', 'week_beginning', 'day'),)

    id = database.Column(database.Integer, primary_key=True)
    camp_id = database.Column(database.Integer, nullable=False)
    week_beginning = database.Column(database.Date, nullable=False)
    day = database.Column(database.String(9), nullable=False)
    employees_booked = database.Column(database.Integer, nullable=False)
