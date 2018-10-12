from os.path import dirname, join
from flask import Flask
from . import db



app = Flask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI="sqlite:///" + join(dirname(dirname(__file__)), "database.sqlite"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(app)

from . import views