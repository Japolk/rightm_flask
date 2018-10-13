from click import command, echo
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

db = SQLAlchemy()


class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    canonical_url = db.Column(db.String(255), unique=True)
    listing_type = db.Column(db.String(12))
    price = db.Column(db.String(50))
    agency_name = db.Column(db.String(50))
    image_links = db.Column(db.Text)

    def __repr__(self):
        return f'{self.id}: {self.price}'

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'canonical_url': self.canonical_url,
           'listing_type'  : self.listing_type,
           'price': self.price,
           'agency_name': self.agency_name,
           'image_links': self.image_links,
       }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()




@command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    echo("Initialized the database.")


def init_app(app):
    """Initialize the Flask app for database usage"""
    db.init_app(app)
    app.cli.add_command(init_db_command)