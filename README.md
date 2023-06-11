# WikiArtistSearch
A Wikipedia scraper that searches for related musical artists written in Python.

WAS uses the Beautiful Soup 4 and Wikipedia modules in Python to take a Wikipedia page selected by the user and recursively search Wikipedia for related pages.
These packages can only function together on Python 3.9.
The constant variables at the start of the code can be modified to allow the scraper to find more pages, although this can significantly increase the time it takes to run.
The code is relatively unoptimized, although with the bottlenecked times from the internet this likely has no effect on runtime.
By default, WAS searches for a maximum of 5 minutes, and can be modified to any number, as well as infinite if set to a negative number.

The function scrapeWikiArticle() is based on the scraper written by Dirk Hoekstra in this article: https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/.
The function sortLists() is based on the bubble sort written by Santiago Valdarrama in this article: https://realpython.com/sorting-algorithms-python/#the-bubble-sort-algorithm-in-python.
The use of the Wikipedia package was largely drawn from this documentation: https://pypi.org/project/wikipedia/.
All of the logic used in the scrapeWikiArticle() function to determine valuable pages and record important occurances was written by me, and required extensive research on Wikipedia pages to find common header trends and templates.

This project was used as a learning exercise for interacting with the internet through code, as well as giving me some training experience with Python.
Any suggestions or criticisms are welcome!
