'''
This class is a basic wrapper around the crawler and analyzer to
to enclose the entire crawling, analyzing, and updating process
into one run() function.
'''

import queue
import requests

from analyzer import analyzer
from crawler import article_finder



DEPTH = 1
NUM_THREADS = 20
POST_URL =  "https://crawler-concurrency.herokuapp.com/add_mention"
GET_COMP_URL = "https://crawler-concurrency.herokuapp.com/get_companies"

class Wrapper:

    def __init__(self):
        self.DB_URL = POST_URL
        response = requests.get(GET_COMP_URL)
        self.stock_names = [i["name"] for i in response.json()["data"]]
        #self.stock_names = ["Apple Inc.", "Amazon", "Tesla", "Google LLC."]

    def run(self):
        articles_queue = queue.Queue()
        crawler = article_finder. ArticleFinder(DEPTH)
        a       = analyzer.Analyzer(self.stock_names, articles_queue, NUM_THREADS,
                   self.DB_URL)

        a.start()
        crawler.find_articles(articles_queue)
        a.join()