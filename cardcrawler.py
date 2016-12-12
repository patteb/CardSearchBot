import requests
from urllib import urlretrieve
from bs4 import BeautifulSoup

def crawler(query, max_pages):
    page = 1
    j = 0
    #initialisierung der Ergebnisse als set, sodass Links auf bilder nur jeweils einmal gespeichert werden
    #Ansonsten gibt es aufgrund der beschaffenheit von magiccards.info fuer suchen mit <30 ergebnissen aber
    #max_pages > 1 die selben ergebnisse max_pages-mal
    matches = set()
    while page <= max_pages:
        #hole den seitenquelltext vom suchaufruf
        url = "http://magiccards.info/query?q=%2B%2B" + query + "&v=scan&s=cname&p=" + str(page)
        page_src = requests.get(url)
        src_txt = page_src.text
        soup = BeautifulSoup(src_txt, "html.parser")
        #finde alle bilder (nur kartenscans!) in diesem quelltext und liste sie im set matches auf
        for image in soup.findAll("img", {"src": lambda L: L and L.startswith("http://magiccards.info/scans/")}):
            matches.add(image.get("src"))
        page += 1

    if len(matches) != 0:
        print( str(len(matches)) + " matches found.")
        print("Downloading images...")
        i = 1
        files = list()
        for img_url in matches:
            #fuer jedes element in matches das bild aus dem netz herunterladen
            img_file = query + str(i) + ".jpg"
            files.append(img_file)
            urlretrieve(img_url,img_file)
            print("\tImage "+str(i)+"/"+str(len(matches))+" done." )
            i += 1
        #Rueckgabe einer liste mit dateinamen der Ergebnisse
        return(files)
    else:
        return 0

#print(crawler("Kraftwerk", 3))