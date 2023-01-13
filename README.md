# Flask Example for rdbbeat

This is a simple example of how to use `rdbbeat` with `Flask`.

## Getting Started with rdbbeat

* Clone this repo
* Start Redis on `localhost:6379/0`
* Start postgres database and update the `DATABASE_URL` in `db_connection.py`
* Install the requirements in `requirements.txt` (preferably in a virtualenv)
* Run `rdbbeat` migration: `python -m alembic -n scheduler upgrade head`
* Run the example's migrations: `python -m flask db upgrade` 

## Running the example
* Open 3 different terminals and run each command in each.
* Run the flask server: `python -m flask run`
* Run the celery worker: `python -m celery --app=server.tasks worker --loglevel=info`
* Run celery beat with custom scheduler: `python -m celery --app=server.tasks beat --loglevel=info --scheduler=rdbbeat.schedulers:DatabaseScheduler`
