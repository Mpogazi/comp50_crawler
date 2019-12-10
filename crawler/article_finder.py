import sys
import threading
from queue import Queue
from crawler.crawler import Crawler
from crawler.util import *

THREADS = 8

NUM_THREADS = 8

class ArticleFinder():

    def __init__(self, depth):
        self.depth = depth

    # Create worker threads (will die when main exits)
    def create_workers(self, num_threads, queue, articles_queue):
        for _ in range(num_threads):
            t = threading.Thread(target=self.work, args=(queue, articles_queue,))
            t.daemon = True
            t.start()

    # Do the next job in the queue
    def work(self, queue, articles_queue):
        while True:
            url = queue.get()
            Crawler.crawl_page(url, articles_queue)
            queue.task_done()

    # Each queued link is a new job
    def create_jobs(self, curr_depth, queue, queue_file):
        for link in file_to_set(queue_file):
            queue.put(link)
        queue.join()
        self.crawl(curr_depth, queue, queue_file)

    # Check if there are items in the queue, if so crawl them
    def crawl(self, curr_depth, queue, queue_file):
        #print("CURR_self.depth_IS -  " + str(curr_depth))
        queued_links = file_to_set(queue_file)
        if len(queued_links) > 0:
            #print(str(len(queued_links)) + ' links in the queue')
            if curr_depth < self.depth:
                self.create_jobs(curr_depth + 1, queue, queue_file)

    def crawl_publication(self, project_name, homepage, num_threads, article_dir, articles_queue):
        domain_name  = get_domain_name(homepage)
        queue_file   = project_name + '/queue.txt'
        queue        = Queue()
        Crawler(project_name, homepage, domain_name, article_dir, articles_queue)
        self.create_workers(num_threads, queue, articles_queue)
        self.crawl(0, queue, queue_file)

    def find_articles(self, articles_queue):
<<<<<<< HEAD
        publications = [("kiplinger", "https://kiplinger.com", NUM_THREADS, "article"),
                        ("thestreet", "https://thestreet.com", NUM_THREADS, "investing"),
                        ("economist", "https://economist.com", NUM_THREADS, "finance-and-economics"),
                        ("marketwatch", "https://www.marketwatch.com", NUM_THREADS, "story")]
        #                ("cabotwealth", "https://www.cabotwealth.com", NUM_THREADS, "growth-stocks")]
=======
        publications = [("kiplinger", "https://kiplinger.com", THREADS, "article"),
                        ("thestreet", "https://thestreet.com", THREADS, "investing"),
                        ("economist", "https://economist.com", THREADS, "finance-and-economics"),
                        ("marketwatch", "https://www.marketwatch.com", THREADS, "story"),
                        ("cabotwealth", "https://www.cabotwealth.com", THREADS, "growth-stocks")]
>>>>>>> 3cf2527182b12cc5b249f76b5fdd2018ffbd1ded
        for i in publications:
            proj_name, homepage, num_threads, article_dir = i
            self.crawl_publication(proj_name, homepage, num_threads, article_dir, articles_queue)

        articles_queue.put("ANALYZER_STOP")
