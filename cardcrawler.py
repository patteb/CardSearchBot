# coding: utf8
import requests
from urllib import urlretrieve
from bs4 import BeautifulSoup


# run a query on maggiccards info and extract all card images
# ---------------------------
# IN: List of already imread() images
# OUT: List of downloaded card image files
def crawler(url, max_pages):
    page = 1
    j = 0
    # initializing the results as set, so links to images are saved only once
    # otherwise there would be multiples of any single card, when there are < 30 hits with max_pages > 1
    # (pages will be crawled multiple times)
    matches = set()
    while page <= max_pages:
        # get html source code
        page_src = requests.get(url + str(page))
        src_txt = page_src.text
        soup = BeautifulSoup(src_txt, "html.parser")
        # find all cardscans in source and list 'em in set "matches"
        # for image in soup.findAll("img", {"src": lambda L: L and L.startswith("http://magiccards.info/scans/")}):
        for image in soup.findAll("img", {"src": lambda L: L and L.startswith("/scans/")}):
            matches.add("http://magiccards.info" + image.get("src"))
        page += 1

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
