import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from server.db_connection import DATABASE_URL
from server.models import db

load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# Celery configuration
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "database"
app.config["CELERY_RESULT_DBURI"] = DATABASE_URL
app.config["CELERY_TRACK_STARTED"] = True
app.config["CELERY_SEND_EVENTS"] = True
app.config["BROKER_TRANSPORT_OPTIONS"] = {"visibility_timeout": 3600}
app.config["CELERY_DEFAULT_QUEUE"] = "default"

migrate = Migrate(app, db, directory="server/migrations", compare_type=True)


CORS(app)
db.init_app(app)

from server.views import employee_router  # noqa isort:skip

app.register_blueprint(employee_router)


@app.route("/")
def index():
    return "Learn to use the celery-rdbbeat scheduler!"
