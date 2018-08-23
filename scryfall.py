from json import load
from urllib import urlopen, urlretrieve


# run a query on scryfall and extract all card images
# ---------------------------
# IN: url of query (including query)
# OUT: List of downloaded card image files
def crawler(url):
    # retrievin JSON data
    req = urlopen(url)
    data = load(req)

    # extracting Image-URL from JSON
    matches = set()
    for i in range(0, data['total_cards']):
        matches.add(data['data'][i]['image_uris']['border_crop'])

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
