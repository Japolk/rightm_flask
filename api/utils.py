import csv
import os
import re
import time
import requests
from lxml import html
from .db import Listing



def get_listig_id(url):
    """return listing id or None from the full url """
    listing_id = re.search(r'property-(\d+).html', url)
    if not listing_id:
        return None
    return int(listing_id.group(1))


def get_listing_type(url):
    """return listing type or None from the full url"""
    listing_type = re.search(r'property-(to|for)-([a-z]+)\/', url)
    if not listing_type:
        return None
    return (listing_type.group(2))


def get_listing_price(tree):
    """get listing price from the rightmove page-tree"""
    try:
        price = tree.xpath(
            "//p[@id='propertyHeaderPrice']/strong")[0].text.strip()
        return price
    except IndexError:
        return ''


def get_listing_agency(tree):
    """get listing agency from the rightmove page-tree"""
    try:
        agency = tree.xpath(
            "//a[@id='aboutBranchLink']/strong")[0].text.strip()
        return agency
    except IndexError:
        return ''


def get_listing_image_links(tree):
    """get listing image urls from the rightmove page-tree"""
    links = ''
    image_links = tree.xpath("//meta[@property='og:image']")
    for image_link in image_links:
        try:
            big_image_link = re.sub(
                r'135x100', '656x437', image_link.attrib['content'])
        except KeyError:
            big_image_link = ''
        links += big_image_link + ', '
    return links


def get_listing_from_db(id):
    """return listing from the DB if it's already there"""
    listing_item = Listing.query.filter_by(id=id).first()
    return listing_item


def get_listing_from_rightmove(url):
    """Parse Rightmove and return Listing object"""
    id = get_listig_id(url)
    type = get_listing_type(url)
    if None in (id, type):
        return None
    """Page Parsing"""
    start_request = time.time()
    html_page = requests.get(url).content
    end_request = time.time()
    duration = round(end_request - start_request, 2)
    log_request_time_to_file(duration, 'External')
    request_limit_timer()
    tree = html.fromstring(html_page)

    price = get_listing_price(tree)
    agency = get_listing_agency(tree)
    links = get_listing_image_links(tree)
    listing_item = Listing(id=id,
                           canonical_url=url,
                           listing_type=type,
                           price=price,
                           agency_name=agency,
                           image_links=links,
                           )
    return listing_item


def make_response(response):
    if isinstance(response, str):
        return {'message': response}, 404
    if isinstance(response, list):
        return {'listings':
                [part.serialize if isinstance(
                    part, Listing) else part for part in response]
                }, 200
    return {'message': 'something gone wrong'}, 404


def save_db_to_csv_file(filename):
    listings_csv = open(f'{filename}', 'w')
    outcsv = csv.writer(listings_csv)
    outcsv.writerow(['id',
                     'canonical_url',
                     'listing_type',
                     'price',
                     'agency_name',
                     'image_links',
                     ])

    result = Listing.query.all()
    for item in result:
        outcsv.writerow([item.id,
                         item.canonical_url,
                         item.listing_type,
                         item.price,
                         item.agency_name,
                         item.image_links,

                         ])
    listings_csv.close()


def log_request_time_to_file(request_time, request_type):
    log_file = open('requests_time_log.txt', 'a')
    current_time = time.strftime("%d.%m.%Y %H:%M:%S")
    log_file.write(
        f'[{current_time}] {request_type} request time: {request_time}\n')
    print(f'[{current_time}] {request_type} request time: {request_time}')
    log_file.close()


def request_limit_timer():
    try:
        requests_limit = int(os.environ.get('REQUESTS_LIMIT'))
    except:
        requests_limit = 10
    delay = 60/requests_limit
    time.sleep(delay)
