# Author: Gibson Smith
# Published: 6/11/2023
# Sources:
    # Dirk Hoekstra's wikipedia scraper (https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/)
    # Santiago Valdarrama's bubble sort algorithm (https://realpython.com/sorting-algorithms-python/#the-bubble-sort-algorithm-in-python)

import requests
import time
import random
from bs4 import BeautifulSoup
import wikipedia

MAX_RECURSION = 2 # modifies depth of searches
MAX_LOOPS = 10 # modifies amount of information pulled from each page
MAX_TIME = 5 # time limit (in minutes) will return after reached
SHOW_ALL = False # debug output

names = [] # name of searched artist
nameshref = [] # name compatible with hrefs
refs = [] # number of references back to original
occs = [] # number of occurances in all pages
hrefs = [] # list of hrefs, prevents redundancy
dist = [] # number of recursive searches to find the name
completion = 0 # for progress bar
keyname = ""
startbench = 0
endbench = 0




# Recursive scrape function
def scrapeWikiArticle(urlend, iterations):
    # Uses BeautifulSoup to parse the Wikipedia page
    url = "https://en.wikipedia.org" + urlend
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Gather relevant section headers to see if the page is worth using
    # album/ep/demo/compilation etc             personnel, track listing
    # song                                      certifications, charts, release and reception, lyrics
    # any person                                career, credits, biography, early life
    # genre                                     characteristics, etymology
    # record label                              artists, acts, recordings, former artists

    # festivals                                 history, organization
    # tours                                     setlist, tour dates
    # playing styles                            see also, techniques
    # instruments/equipment                     theory
    title = soup.find(id="firstHeading")
    if iterations == 0:
        keyname = title.text
    # artist
    discog = soup.find(id="Discography")
    # album/ep/demo/compilation/single etc
    personnel = soup.find(id="Personnel")
    tracklist = soup.find(id="Track_listing")
    # song
    certifications = soup.find(id="Certifications")
    charts = soup.find(id="Charts")
    release = soup.find(id="Release_and_reception")
    # person
    career = soup.find(id="Career")
    credits = soup.find(id="Credits")
    biog = soup.find(id="Biography")
    early = soup.find(id="Early_life")
    #genre
    character = soup.find(id="Characteristics")
    etymology = soup.find(id="Etymology")
    #record label
    artists = soup.find(id="Artists")
    acts = soup.find(id="Acts")
    recordings = soup.find(id="Recordings")
    former = soup.find(id="Former_artists")
    # festivals/tours
    setlist = soup.find(id="Setlist")
    tour = soup.find(id="Tour_dates")
    # instruments/techniques/equipment
    see = soup.find(id="See_also")
    techniques = soup.find(id="Techniques")
    theory = soup.find(id="theory")


    # Ends search if current child is not an "important" page
    # Ignored for the first iteration, so you can choose any Wikipedia page
    if SHOW_ALL == True:
        print(title.text, end="")
    if (discog != None or personnel != None or tracklist != None or
        certifications != None or charts != None or release != None or
        career != None or credits != None or biog != None or early != None or 
        character != None or etymology != None or artists != None or 
        acts != None or recordings != None or former != None or
        setlist != None or tour != None or see != None or techniques != None or
        theory != None) != True and iterations > 0:
        if SHOW_ALL == True:
            print("")
        return
    if SHOW_ALL == True:
        print("- OK")
    if discog != None: # is an artist, add to names
        names.append(title.text)
        nameshref.append(urlend)
        refs.append(0)
        occs.append(0)
    if iterations > MAX_RECURSION:
        return
    

    # Recursively scrapes children
    allLinks = soup.find(id="bodyContent").find_all("a")
    random.shuffle(allLinks)
    linkToScrape = None
    loops = 0
    for link in allLinks:
        # Controls how many links can be scraped per page
        if loops > MAX_LOOPS:
            break
        # Time limit check
        bench = time.time()
        elapsed = bench - startbench
        global completion
        if (elapsed > (60 * MAX_TIME) and MAX_TIME > 0):
            break
        elif (((elapsed / (60 * MAX_TIME)) * 10) > completion and SHOW_ALL == False):
            print("[", end="")
            for i in range(completion):
                print("#", end="")
            for i in range(10 - completion):
                print("-", end="")
            print("]")
            completion += 1
        if 'href' not in link.attrs:  # Check if 'href' attribute exists
            continue
        # Prevents searches that could break the scraper
        if link['href'].find("/wiki/") == -1 or link['href'].find("https:") >= 0:
            continue
        if (link['href'].find("Help:") >= 0 or link['href'].find("Category:") >= 0 or
            link['href'].find("Special:") >= 0 or link['href'].find("File:") >= 0 or
            link['href'].find("Wikipedia:") >= 0 or link['href'].find("Template:") >= 0 or
            link['href'].find("Template_talk:") >= 0 or link['href'].find("Talk:") >= 0 or
            link['href'].find("Portal:") >= 0) == True:
            continue
        linkToScrape = link
        if linkToScrape is not None:
            # Reference/Occurance Logic
            if linkToScrape['href'] in hrefs:
                if linkToScrape['href'] == key and discog != None: # reference to key
                    refs[nameshref.index(urlend)] += 1
                elif linkToScrape['href'] in nameshref: # occurance of name in other page
                    occs[nameshref.index(linkToScrape['href'])] += 1
            # Scrape new pages as children
            else:
                hrefs.append(linkToScrape['href'])
                if SHOW_ALL == True:
                    numits = ""
                    for i in range(iterations):
                        numits = numits + "_________________________________________________________________"
                    print(numits, "added ", linkToScrape['href'], " to list")##
                loops += 1
                scrapeWikiArticle(linkToScrape['href'], iterations + 1)



# sorts the names list based on the combined results of occs and refs
def sortlists():
    size = len(occs)
    for i in range(size):
        sorted = True
        for j in range(size - i - 1):
            if occs[j] < occs[j + 1]:
                occs[j], occs[j + 1] = occs[j + 1], occs[j]
                names[j], names[j + 1] = names[j + 1], names[j]
                sorted = False
        if sorted:
            break
    return



# Main Sequence
print("Enter a wikipedia page to start the search?")
userin = input()
options = wikipedia.search(userin)
print("Which of these pages do you want to search? (Choose from 1 to 10)", options)
userchoice = input()
print(options[int(userchoice) - 1])
key = wikipedia.page(options[int(userchoice) - 1]).url.removeprefix("https://en.wikipedia.org")
print("Recursive Scraping for ", key, ", max recursion = ", MAX_RECURSION, ", max pages = ", MAX_LOOPS, ", time limit = ", (MAX_TIME * 60), " seconds")
startbench = time.time()
scrapeWikiArticle(key, 0)
size = len(names)
endbench = time.time()
elapsed = endbench - startbench
if SHOW_ALL == True:
    print()
    print(names)
    print(nameshref)
    print("Refs", refs)
    print("Occs", occs)
    # Rank final names
    for i in range(size):
        occs[i] = occs[i] + refs[i]
    #for j in occs:
    print("Combined: ", occs)
    sortlists()
    print("Sorted:")
    print(names)
    print(occs)
    print()
else:
    print("[##########]")
count = 0
print("You searched: ", keyname)
print(len(hrefs), " pages read")
print(size, " artists found")
print("Time: ", elapsed)
print("Recommended artists: ")
for i in range(size):
    if names[i] == keyname:
        continue
    print(names[i])
    count += 1
    if count == 20:
        break
