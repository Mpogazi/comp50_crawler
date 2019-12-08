import sys
import threading
from queue import Queue
from crawler import Crawler
from util import *

DEPTH = 1

# Create worker threads (will die when main exits)
def create_workers(num_threads, queue, articles_queue):
    for _ in range(num_threads):
        t = threading.Thread(target=work, args=(queue, articles_queue,))
        t.daemon = True
        t.start()


# Do the next job in the queue
def work(queue, articles_queue):
    while True: 
        url = queue.get()
        Crawler.crawl_page(threading.current_thread().name, url, articles_queue)
        queue.task_done()


# Each queued link is a new job
def create_jobs(curr_depth, queue, queue_file):
    for link in file_to_set(queue_file):
        queue.put(link)
    queue.join()    
    crawl(curr_depth, queue, queue_file)


# Check if there are items in the queue, if so crawl them
def crawl(curr_depth, queue, queue_file):
    print("CURR_DEPTH_IS -  " + str(curr_depth))
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        if curr_depth < DEPTH:
            create_jobs(curr_depth + 1, queue, queue_file)


def run(project_name, homepage, num_threads, article_dir, articles_queue):
    domain_name  = get_domain_name(homepage)
    queue_file   = project_name + '/queue.txt' 
    queue        = Queue()
    threads      = []

    Crawler(project_name, homepage, domain_name, article_dir, articles_queue)
    create_workers(num_threads, queue, articles_queue)
    crawl(0, queue, queue_file)    

#    Crawler.articles.add("ANALYZER_STOP")

def main():
    publications = [("kiplinger", "https://kiplinger.com", 10, "article"),
                    ("thestreet", "https://thestreet.com", 10, "investing"),
                    ("economist", "https://economist.com", 10, "finance-and-economics"),
                    ("marketwatch", "https://www.marketwatch.com", 10, "story")]
#                    ("seekingalpha", "https://www.seekingalpha.com", 10, "article")


    articles_queue = Queue() 
  #  forbes_thread  = threading.Thread(target=run, args=forbes)
    for i in publications:
        proj_name, homepage, num_threads, article_dir = i
        run(proj_name, homepage, num_threads, article_dir, articles_queue) 


    article_file = open("articles.txt", "w")
    for article in articles_queue.queue:
        article_file.write(article + '\n')
    article_file.close() 
    #forbes_thread.start()

    


if __name__ == '__main__':
    main()     
