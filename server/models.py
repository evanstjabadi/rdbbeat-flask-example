from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "date_of_birth": self.date_of_birth.strftime("%Y-%m-%d"),
        }
