from flask_restful import Resource, Api, reqparse
from . import app
from .db import db, Listing
from .utils import get_listing_agency, get_listig_id, get_listing_image_links, get_listing_price, get_listing_type

api = Api(app)


class ListingView(Resource):

    def get(self):
        return 'hello, world!'

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)
        url = parser.parse_args()['url']
        id = get_listig_id(url)
        type = get_listing_type(url)
        price = get_listing_price(url)
        agency = get_listing_agency(url)
        links = get_listing_image_links(url)
        print(f'id: {id}, type: {type}, price: {price}, agency: {agency}\n links:{links}')
        return id

api.add_resource(ListingView, '/')