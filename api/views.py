from flask_restful import Resource, Api, reqparse
from . import app
from .db import Listing
from .utils import get_listing_from_rightmove, return_if_listing_is_in_db, make_response

api = Api(app)


class ListingView(Resource):

    def get(self):
        listings = Listing.query.all()
        print(listings[0].price)
        return {'listing' : 'okay'}, 200


    def post(self):
        """Request Parsing"""
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)
        listing_url = parser.parse_args()['url']
        print(parser.parse_args())
        if not listing_url:
            return make_response('bad request!!!11')

        """Check if listing is already in DB"""
        listing_item = return_if_listing_is_in_db(listing_url)
        if listing_item:
            return make_response(listing_item)

        """Get listing form RightMove and save to DB"""
        listing_item = get_listing_from_rightmove(listing_url)
        if not listing_item:
            return make_response('bad url')
        listing_item.save_to_db()
        return make_response(listing_item)

api.add_resource(ListingView, '/')