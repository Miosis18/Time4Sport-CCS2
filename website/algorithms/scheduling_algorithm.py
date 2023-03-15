from collections import defaultdict
from website.management.database_management import database
from website.models.database_models import EmployeeAvailability, CampAvailabilityRequirements, Schedule, ShortDays


def create_schedules() -> None:

    database.session.query(Schedule).delete()
    database.session.query(ShortDays).delete()

    # Convert rows to CampAvailabilityRequirements and EmployeeAvailability objects

    camps = database.session.query(CampAvailabilityRequirements).all()
    employees = database.session.query(EmployeeAvailability).all()

    # Creates a dictionary of employees that are available to work on a specific day for each week.

    available_employees = defaultdict(list)

    day_map = {
        'Monday': 'monday',
        'Tuesday': 'tuesday',
        'Wednesday': 'wednesday',
        'Thursday': 'thursday',
        'Friday': 'friday',
        'Saturday': 'saturday',
        'Sunday': 'sunday',
    }

    for employee in employees:
        for day, attribute in day_map.items():
            if getattr(employee, attribute) is True:
                available_employees[(employee.week_beginning, day)].append(employee)

    # Book upto 3 employees per camp per day that they are required.

    for camp in camps:
        camp_booked_employees = defaultdict(list)

        for day, attribute in day_map.items():
            if getattr(camp, attribute) is True:
                key = (camp.week_beginning, day)
                employees_available_on_required_day = available_employees[key]
                number_of_employees_required = 3 - len(camp_booked_employees[key])
                employees_to_schedule = employees_available_on_required_day[:number_of_employees_required]

                for employee in employees_to_schedule:
                    existing_schedule = database.session.query(Schedule).filter_by(
                        employee_id=employee.employee_id,
                        camp_id=camp.camp_id,
                        week_beginning=employee.week_beginning,
                        scheduled_day=day).first()

                    if existing_schedule:
                        # Overwrite the existing schedule
                        existing_schedule.employee_id = employee.employee_id
                        existing_schedule.camp_id = camp.camp_id
                        existing_schedule.week_beginning = employee.week_beginning
                        existing_schedule.scheduled_day = day

                    else:
                        # Add a new schedule
                        new_schedule = Schedule(employee_id=employee.employee_id, camp_id=camp.camp_id,
                                                week_beginning=employee.week_beginning, scheduled_day=day)
                        database.session.add(new_schedule)

                    camp_booked_employees[key].append(employee)
                    employees_available_on_required_day.remove(employee)

    # Check camp has enough employees for each day that employees are required

        for day, attribute in day_map.items():
            if getattr(camp, attribute) is True:
                key = (camp.week_beginning, day)
                if len(camp_booked_employees[key]) < 3:

                    existing_short_day = database.session.query(ShortDays).filter_by(
                        camp_id=camp.camp_id,
                        week_beginning=camp.week_beginning,
                        day=day).first()

                    if existing_short_day:
                        # Overwrite the existing schedule
                        existing_short_day.camp_id = camp.camp_id
                        existing_short_day.week_beginning = camp.week_beginning
                        existing_short_day.scheduled_day = day
                        existing_short_day.employees_booked = len(camp_booked_employees[key])

                    else:
                        new_short_day = ShortDays(camp_id=camp.camp_id, week_beginning=camp.week_beginning, day=day,
                                                  employees_booked=len(camp_booked_employees[key]))
                        database.session.add(new_short_day)

    database.session.commit()


# Example usage
create_schedules()

schedules = database.session.query(Schedule).all()

# Print schedules
for schedule in schedules:
    print(f"Employee {schedule.employee_id} scheduled for {schedule.scheduled_day} at Camp {schedule.camp_id} on "
          f"{schedule.week_beginning}")

short_days = database.session.query(ShortDays).all()

# Print short days
for short_day in short_days:
    print(f"Camp {short_day.camp_id} scheduled for {short_day.day} beginning week {short_day.week_beginning} is short "
          f"by {3 - short_day.employees_booked} {'employee' if (3 - short_day.employees_booked) == 1 else 'employees'}")
