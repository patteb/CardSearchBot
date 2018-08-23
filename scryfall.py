# coding=utf-8

from json import load
from urllib import urlopen, urlretrieve


# Contruct an url from the query
# ---------------------------
# IN: url-pre-snippet from config, query
# OUT: url to hand of to crawler
def build_query(pre, query):
    # resolving the query
    print("Querying the first page(s) of \"" + query + "\" on scryfall")
    # constructing the url
    url = pre + query.replace(" ", "+")

    return url


# run a query on scryfall and extract all card images
# ---------------------------
# IN: url of query (including query)
# OUT: List of image url
def crawler(url):
    # retrievin JSON data
    req = urlopen(url)
    data = load(req)

    # extracting Image-URL from JSON
    matches = set()
    for i in range(0, data['total_cards']):
        matches.add(data['data'][i]['image_uris']['border_crop'])
    return matches


# Contruct an url from the query
# ---------------------------
# IN: list of image urls
# OUT: list of image files

def card_download(matches):
    # download Images
    if len(matches) != 0:
        print(str(len(matches)) + " matches found.")
        print("Downloading images...")
        i = 1
        files = list()
        for img_url in matches:
            # download image for every element in matches
            img_file = "temp/" + str(i) + ".jpg"
            files.append(img_file)
            urlretrieve(img_url, img_file)
            print("\tImage " + str(i) + "/" + str(len(matches)) + " done.")
            i += 1
        # return a list of filenames
        return (files)
    else:
        return 0
