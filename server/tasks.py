from server.celery_worker import app
from server.models import Employee, db
from server.session_management import session_scope


@app.task(name="birthday_greeting")
def birthday_greeting(employee_id):
    with session_scope() as session:
        employee = session.query(Employee).get(employee_id)
        print(f"Happy birthday, {employee.name} {employee.surname}!")

    # Send email to employee
    # email_service.send_email(template="birthday_greeting", to=employee.email, context={"employee": employee.to_dict()})
    # Remind his manager too!
