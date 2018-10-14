import csv, re, requests
from lxml import html
from .db import Listing

def get_listig_id(url):
    """return listing id from the full url or None"""
    listing_id = re.search(r'property-(\d+).html',url)
    if not listing_id:
        return None
    return int(listing_id.group(1))


def get_listing_type(url):
    """return listing type from the full url or None"""
    listing_type = re.search(r'property-(to|for)-([a-z]+)\/',url)
    if not listing_type:
        return None
    return (listing_type.group(2))


def get_listing_price(url):
    """get listing price from the rightmove site"""
    html_page= requests.get(url).content
    tree = html.fromstring(html_page)
    try:
        price = tree.xpath("//p[@id='propertyHeaderPrice']/strong")[0].text.strip()
        return price
    except IndexError:
        return ''

def get_listing_agency(url):
    """get listing agency from the rightmove site"""
    html_page= requests.get(url).content
    tree = html.fromstring(html_page)
    try:
        agency = tree.xpath("//a[@id='aboutBranchLink']/strong")[0].text.strip()
        return agency
    except IndexError:
        return ''


def get_listing_image_links(url):
    """get listing image urls from the rightmove site"""
    links = ''
    html_page= requests.get(url).content
    tree = html.fromstring(html_page)
    image_links = tree.xpath("//meta[@property='og:image']")
    for image_link in image_links:
        try:
            big_image_link = re.sub(r'135x100', '656x437', image_link.attrib['content'])
        except KeyError:
            big_image_link = ''
        links += big_image_link + ', '
    return links


def get_listing_from_db(id):
    """return listing from the Db if it's already there"""
    listing_item = Listing.query.filter_by(id=id).first()
    return listing_item


def get_listing_from_rightmove(url):
    """Parse Rightmove and return Listing object"""
    id = get_listig_id(url)
    type = get_listing_type(url)
    if None in (id, type):
        return None
    price = get_listing_price(url)
    agency = get_listing_agency(url)
    links = get_listing_image_links(url)
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
        return {'listings': [part.serialize if isinstance(part, Listing) else part for part in response ]}, 200
    return {'message':'ALL GONE WRONG'}, 404



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