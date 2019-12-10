'''
This class is a basic wrapper around the crawler and analyzer to
to enclose the entire crawling, analyzing, and updating process
into one run() function.

To use as a standalone program, run

    python3 wrapper.py [stock-name] [stock-name] ...

Where each [stock-name] is a stock to watch. MAKE SURE this matches
the company's name as listed in S&P 500. AND spaces should be represented as
a '-' character.

Example: if you care about Google and Amazon, run

    python3 wrapper.py Alphabet-Inc. Amazon.com-Inc.
'''

import queue
import requests
import sys

from analyzer import analyzer
from crawler import article_finder



DEPTH = 1
NUM_THREADS = 20
POST_URL =  "https://crawler-concurrency.herokuapp.com/add_mention"
GET_COMP_URL = "https://crawler-concurrency.herokuapp.com/get_companies"

class Wrapper:

    def __init__(self, watchlist = ["Apple Inc.", "Amazon.com Inc.",
                                    "Alphabet Inc.", "PayPal"]):
        self.DB_URL = POST_URL
        response = requests.get(GET_COMP_URL)
        self.stock_names = [i["name"] for i in response.json()["data"]]
        self.watchlist = watchlist
        self.data = {}


    def run(self):
        articles_queue = queue.Queue()
        crawler = article_finder.ArticleFinder(DEPTH)
        a       = analyzer.Analyzer(self.stock_names, articles_queue, NUM_THREADS,
                   self.DB_URL)

        a.start()
        crawler.find_articles(articles_queue)
#<<<<<<< HEAD
        a.join()
        self.data = a.get_data()

    def print_results(self):
        f = open("articles_for_you.txt", "w+")
        for stock in self.watchlist:
            if stock not in self.data.keys():
                continue
            f.write(stock + "\n")
            for article in self.data[stock]["update"]:
                f.write(article["article_title"] + "\n")
                f.write(article["article_url"] + "\n")

            f.write("\n")
        f.close()


if __name__ == "__main__":
    watchlist = []
    for i in range(1, len(sys.argv)):
        watchlist.append(" ".join(sys.argv[i].split("-")))
    if len(watchlist) == 0:
        prog = Wrapper()
    else:
        prog = Wrapper(watchlist)
    prog.run()
    prog.print_results()
#=======
#        a.join()
#>>>>>>> 78959c2e749f50e55f17ad133dd93a990c8cc7ac
