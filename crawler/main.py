import sys
import threading
from queue import Queue
from crawler import Crawler
from util import *


# Create worker threads (will die when main exits)
def create_workers(num_threads, queue):
    for _ in range(num_threads):
        t = threading.Thread(target=work, args=(queue,))
        t.daemon = True
        t.start()


# Do the next job in the queue
def work(queue):
    while True:
        url = queue.get()
        Crawler.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs(queue, queue_file):
    for link in file_to_set(queue_file):
        queue.put(link)
    queue.join()
    crawl(queue, queue_file)


# Check if there are items in the queue, if so crawl them
def crawl(queue, queue_file):
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs(queue, queue_file)


def run():
    project_name = str(sys.argv[1])
    homepage     = str(sys.argv[2])
    num_threads  = int(sys.argv[3])
    domain_name  = get_domain_name(homepage)
    queue_file   = project_name + '/queue.txt' 
    queue        = Queue()

    Crawler(project_name, homepage, domain_name)
    create_workers(num_threads, queue)
    crawl(queue, queue_file)
    return Crawler.url_list() 


def main():
    urls = run()
    print(urls)
    print(len(urls))
     


if __name__ == '__main__':
    main()     
