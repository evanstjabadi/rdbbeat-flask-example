from dateutil.parser import parse
from flask import Blueprint, jsonify, request
from rdbbeat.controller import Schedule, ScheduledTask, schedule_task

from server.models import Employee
from server.session_management import session_scope

employee_router = Blueprint("employee_router", __name__, url_prefix="/api/v1")


@employee_router.post("/employees/")
def create_employee():
    employee_data = request.get_json()
    date_of_birth = parse(employee_data["date_of_birth"]).date()

    employee = Employee(
        name=employee_data["name"],
        surname=employee_data["surname"],
        date_of_birth=date_of_birth,
    )
    with session_scope() as session:
        session.add(employee)
        session.commit()

        # Create birthday greeting task
        db_employee = session.query(Employee).get(employee.id)
        # schedule = Schedule(
        #     minute="*",
        #     hour="*",
        #     day_of_week="*",
        #     day_of_month=str(date_of_birth.day),
        #     month_of_year=str(date_of_birth.month),
        #     timezone="UTC" # TODO: get timezone from employee
        # )

        # Though above is correct, let's image schedule ran every 1 minute for testing purposes
        schedule = Schedule(
            minute="*",
            hour="*",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone="UTC",
        )

        task_to_schedule = ScheduledTask(
            name=f"{db_employee.id}_birthday_greeting",  # All tasks must have a unique name
            task="birthday_greeting",
            schedule=schedule,
        )
        task_kwargs = {"employee_id": db_employee.id}
        schedule_task(session=session, scheduled_task=task_to_schedule, **task_kwargs)

    return jsonify(db_employee.to_dict()), 201


@employee_router.get("/employees/<int:employee_id>")
def get_employee(employee_id):
    with session_scope() as session:
        employee = session.query(Employee).get(employee_id)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        return jsonify(employee.to_dict())
