import re,requests
from lxml import html

def get_listig_id(url):
    """return listing id(INT) from the full url"""
    result = re.search(r'property-(\d+).html',url)
    return int(result.group(1))


def get_listing_type(url):
    """return listing type (STR) from the full url"""
    result = re.search(r'property-(to|for)-([a-z]+)\/',url)
    return (result.group(2))


def get_listing_price(url):
    html_page= requests.get(url).content
    tree = html.fromstring(html_page)
    price = tree.xpath("//p[@id='propertyHeaderPrice']/strong")[0].text.strip()
    return price

def get_listing_agency(url):
    html_page= requests.get(url).content
    tree = html.fromstring(html_page)
    agency = tree.xpath("//div[@class='agent-details-display']/p[@class='pad-0']/a/strong")[0].text.strip()
    return agency

def get_listing_image_links(url):
    links = []
    html_page= requests.get(url).content
    tree = html.fromstring(html_page)
    image_links = tree.xpath("//meta[@property='og:image']")
    for image_link in image_links:
        big_image_link = re.sub(r'135x100', '656x437', image_link.attrib['content'])
        links.append(big_image_link)
    return links