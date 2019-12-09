

import queue

from analyzer import analyzer
from ../crawler/article_finder import article_finder



DEPTH = 10
NUM_THREADS = 50

class Wrapper:

    def __init__(self, DB_URL):
        self.DB_URL = DB_URL

    def run(self):
        articles_queue = queue.Queue()
        crawler = article_finder.ArticleFinder(DEPTH)
        analyzer = analyzer.Analyzer(stock_names, articles_queue, NUM_THREADS,
                   self.DB_URL)
        crawler.find_articles(articles_queue)
        analyzer.start()
        analyzer.join()
