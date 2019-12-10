import sys
import threading
from queue import Queue
from crawler.crawler import Crawler
from crawler.util import *

NUM_THREADS = 8

class ArticleFinder():

    def __init__(self, depth):
        self.depth = depth

    def create_workers(self, num_threads, queue, articles_queue):
        for _ in range(num_threads):
            t = threading.Thread(target=self.work, 
                                 args=(queue, articles_queue,))
            t.daemon = True
            t.start()

    def work(self, queue, articles_queue):
        while True:
            url = queue.get()
            Crawler.crawl_page(url, articles_queue)
            queue.task_done()

    def create_jobs(self, curr_depth, queue, to_be_crawled):
        for link in to_be_crawled: 
            queue.put(link)
        queue.join()
        self.crawl(curr_depth, queue, to_be_crawled)

    # Check if there are items in the queue, if so crawl them
    def crawl(self, curr_depth, queue, to_be_crawled):
        if len(to_be_crawled) > 0:
            if curr_depth < self.depth:
                self.create_jobs(curr_depth + 1, queue, to_be_crawled)

    def crawl_publication(self, publication, homepage, 
                          num_threads, article_dir, articles_queue):
        domain_name  = get_domain_name(homepage)
        queue        = Queue()
        Crawler(publication, homepage, domain_name, article_dir, 
                articles_queue)
        self.create_workers(num_threads, queue, articles_queue)
        self.crawl(0, queue, Crawler.to_be_crawled)

    def find_articles(self, articles_queue):
        publications = [("kiplinger", "https://kiplinger.com", 
                         NUM_THREADS, "article"),
                        ("thestreet", "https://thestreet.com", 
                         NUM_THREADS, "investing"),
                        ("economist", "https://economist.com", 
                         NUM_THREADS, "finance-and-economics"),
                        ("marketwatch", "https://www.marketwatch.com", 
                         NUM_THREADS, "story")]
        for i in publications:
            publication, homepage, num_threads, article_dir = i
            self.crawl_publication(publication, homepage, num_threads, 
                                   article_dir, articles_queue)
        articles_queue.put("ANALYZER_STOP")
