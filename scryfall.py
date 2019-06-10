# coding=utf-8

from json import load
from urllib import urlopen, urlretrieve


def build_query(pre, query):
    """Construct an url from the query
    ---------------------------
    :param url-pre-snippet from config, query
    :return: url to hand of to crawler"""
    print("Querying \"%s\" on scryfall." % query),
    return pre + query.replace(" ", "+")  # replace necessary for url-handling


def api_query(url):
    """run a query on scryfall and extract all card images
    API documentation @ https://scryfall.com/docs/api
    ---------------------------
    :param url of query (including query)
    :return: List of image url"""
    # retrieving JSON data
    req = urlopen(url)
    data = load(req)

    # check for 0 results
    if data['object'] == 'error':
        print("Error: %s" % data['details'])
        print("Exiting.")
        quit()

    # extracting Image-URL from JSON
    img_url = set()
    for i in range(0, data['total_cards']):
        img_url.add(data['data'][i]['image_uris']['png'])

    return img_url


def card_download(matches):
    """"Download all card images from list, saving in temp-directory
    ---------------------------
    :param list of image urls
    :return: list of image files"""
    if len(matches) != 0:  # check card url list for existing urls
        print("%s matches found." % len(matches))
        print("Downloading images...")
        i = 1
        files = list()
        for img_url in matches:  # iterating through the list, following each url.
            # download image for every element in matches
            img_file = "temp/%s.jpg" % i
            files.append(img_file)
            urlretrieve(img_url, img_file)
            print("\r\tImage %s/%s" % (i, len(matches))),  # trailing comma to omit newline
            i += 1
        # return a list of file names
        print "done!"
        return files
    else:
        return 0


def scryfall(url_pre, query):
    """Combine function to build query, do the API-call and download images
    ---------------------------
    :param url_pre-snippet from config, query
    :return: list of image files"""
    url = build_query(url_pre, query)  # construct query url
    img_url = api_query(url)  # API-Call
    return card_download(img_url)  # download images
