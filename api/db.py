from click import command, echo
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

db = SQLAlchemy()


class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    canonical_url = db.Column(db.String(255), unique=True)
    listing_type = db.Column(db.String(12))
    price = db.Column(db.Integer)
    agency_name = db.Column(db.String(50))
    image_links = db.Column(db.String(250))

    def __repr__(self):
        return f'{self.id}: {self.price}'







@command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    echo("Initialized the database.")


def init_app(app):
    """Initialize the Flask app for database usage."""
    db.init_app(app)
    app.cli.add_command(init_db_command)