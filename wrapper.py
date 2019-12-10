'''
This class is a basic wrapper around the crawler and analyzer to
to enclose the entire crawling, analyzing, and updating process
into one run() function.
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

    def __init__(self, watchlist = ["Apple Inc.", "Amazon",
                                    "Tesla", "Google LLC."]):
        self.DB_URL = POST_URL
        response = requests.get(GET_COMP_URL)
        self.stock_names = [i["name"] for i in response.json()["data"]]
        self.watchlist = watchlist
        self.data = {}


    def run(self):
        articles_queue = queue.Queue()
        crawler = article_finder. ArticleFinder(DEPTH)
        a       = analyzer.Analyzer(self.stock_names, articles_queue, NUM_THREADS,
                   self.DB_URL)

        a.start()
        crawler.find_articles(articles_queue)
        a.join()
        self.data = a.get_data()

    def print_results(self):
        f = open("articles_for_you.txt")
        for stock in self.watchlist:
            if stock not in self.data.keys():
                continue
            f.write(stock)
            for article in self.data[stock]["update"]:
                f.write(article["article_title"] + "\n")
                f.write(article["article_url"] + "\n")

            f.write("\n")
        f.close()


if __name__ == "__main__":
    watchlist = []
    for i in range(1, len(sys.argv)):
        watchlist.append(sys.argv[i])
    if len(watchlist) == 0:
        prog = Wrapper()
    else:
        prog = Wrapper(watchlist)
    prog.run()
    prog.print_results()
