# coding=utf-8

from json import load
from urllib import urlopen, urlretrieve


def build_query(pre, query):
    """Construct an url from the query
    ---------------------------
    IN: url-pre-snippet from config, query
    OUT: url to hand of to crawler"""
    print("Querying \"" + query + "\" on scryfall")
    url = pre + query.replace(" ", "+")  # replace necessary for url-handling

    return url


def api_query(url):
    """run a query on scryfall and extract all card images
    API documentation @ https://scryfall.com/docs/api
    ---------------------------
    IN: url of query (including query)
    OUT: List of image url"""
    # retrieving JSON data
    req = urlopen(url)
    data = load(req)

    # check for 0 results
    if data['object'] == 'error':
        print("Error: " + data['details'])
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
    IN: list of image urls
    OUT: list of image files"""
    if len(matches) != 0:  # check card url list for existing urls
        print(str(len(matches)) + " matches found.")
        print("Downloading images...")
        i = 1
        files = list()
        for img_url in matches:  # iterating through the list, following each url
            # download image for every element in matches
            img_file = "temp/" + str(i) + ".jpg"
            files.append(img_file)
            urlretrieve(img_url, img_file)
            print("\r\tImage " + str(i) + "/" + str(len(matches))),  # trailing comma to omit newline
            i += 1
        # return a list of file names
        print ("done.")
        return files
    else:
        return 0
