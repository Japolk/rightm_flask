import time
from os.path import dirname, join
from flask import Flask, g
from . import db, utils


app = Flask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI="sqlite:///" +
    join(dirname(dirname(__file__)), "database.sqlite"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(app)


@app.before_request
def start_timer():
    g.start = time.time()
    pass


@app.after_request
def log_request(response):
    now = time.time()
    duration = round(now - g.start, 2)
    utils.log_request_time_to_file(duration, 'Internal')
    return response


from . import views
