# Flask Example for rdbbeat

This is a simple example of how to use `rdbbeat` with `Flask`.

## Getting Started with rdbbeat

* Clone this repo
* Install the requirements in `requirements.txt` (preferably in a virtualenv)
* Start Redis on `localhost:6379/0` or update the `REDIS_URL` in the `celery_worker.py` if your url is different
* Start postgres database and put the `DATABASE_URL` in the `.env` file. E.g, `DATABASE_URL="postgresql://username:password@localhost:5432/database"`
* Put `FLASK_APP=server/app.py` in the `.env` file.
* Run `rdbbeat` migration: `python -m alembic -n scheduler upgrade head`
* Run the example's migrations: `python -m flask db upgrade` 

## Running the example
* Open 3 different terminals and run each command in each.
* Run the flask server: `python -m flask run`
* Run the celery worker: `python -m celery --app=server.tasks worker --loglevel=info`
* Run celery beat with custom scheduler: `python -m celery --app=server.tasks beat --loglevel=info --scheduler=rdbbeat.schedulers:DatabaseScheduler`

## Output
<img width="1407" alt="terminals' outputs" src="https://github.com/evanstjabadi/rdbbeat-flask-example/assets/31672668/91393478-a94d-4835-afe1-63209f012fa6">
