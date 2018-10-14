import flask
from flask_restful import Resource, Api, reqparse

from . import app
from .db import db, Listing
from .utils import get_listing_from_rightmove, get_listing_from_db, make_response, get_listig_id, save_db_to_csv_file

api = Api(app)


class ListingView(Resource):

    def get(self):
        filename = 'listings.csv'
        save_db_to_csv_file(filename)
        return flask.send_file(f'../{filename}',
                               as_attachment=True,
                               mimetype='text/csv')

    def post(self):
        listing_list = []
        """Request Parameters Parsing"""
        parser = reqparse.RequestParser()
        parser.add_argument('urls', type=str, action='append')
        listing_urls = parser.parse_args()['urls']
        if not listing_urls:
            return make_response('bad request!!!11')

        """Get listings from Rightmove or from DB"""
        input_listings_dict = {get_listig_id(url): url for url in listing_urls}
        already_saved_listing_ids = [x[0] for x in db.session.query(
            Listing.id).filter(Listing.id.in_(input_listings_dict)).all()]

        for id, url in input_listings_dict.items():
            if id in already_saved_listing_ids:
                listing_list.append(get_listing_from_db(id))
            else:
                listing_item = get_listing_from_rightmove(url)
                """check if come broken links were in request"""
                if listing_item:
                    listing_item.save_to_db()
                    listing_list.append(listing_item)
                else:
                    listing_list.append('wrong link')

        return make_response(listing_list)


api.add_resource(ListingView, '/')