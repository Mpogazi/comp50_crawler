from urllib.request import urlopen
from link_finder import LinkFinder
from util import *

# The Crawler class, given a project name (name of the directory where
# links {queued and crawled} are stored on disc), a base_url, and a 
# domain_name (for the purpose of only compiling links which are subpages
# of the domain name -- Not necessarily what we have in mind for long-term 
# goal), parses base_url for links and queues links in both in memory and 
# on disc.

class Crawler:

    # Class variables (shared among all instances)
    project_name = ''
    base_url     = ''
    domain_name  = ''
    queue_file   = ''
    crawled_file = ''
    queue   = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Crawler.project_name = project_name
        Crawler.base_url     = base_url
        Crawler.domain_name  = domain_name
        Crawler.queue_file = Crawler.project_name + "/queue.txt"
        Crawler.crawled_file = Crawler.project_name + "/crawled.txt"
        self.boot()
        self.crawl_page("First Crawler", Crawler.base_url)

    def boot(self):
        create_project_dir(Crawler.project_name)
        create_data_files(Crawler.project_name, Crawler.base_url)
        Crawler.queue   = file_to_set(Crawler.queue_file)
        Crawler.crawled = file_to_set(Crawler.crawled_file)

    def crawl_page(self, thread_name, page_url):
        if page_url not in Crawler.crawled:
            print(thread_name + " crawling " + page_url)
            print("Queue " + str(len(Crawler.queue)) + " | Crawled " + str(len(Crawler.crawled)))
            Crawler.enqueue_links(self, Crawler.gather_links(self, page_url))
            Crawler.queue.remove(page_url)
            Crawler.crawled.add(page_url)
            Crawler.update_files(self)

    # Connects to site, passes html to linkfinder which parses html for
    # links, then returns set of links. Returns the empty set in case 
    # of error.
    def gather_links(self, page_url):
        html_str = ""
        with urlopen(page_url) as response:
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_str  = html_bytes.decode("utf-8")
            finder = LinkFinder(Crawler.base_url, page_url)
            finder.feed(html_str)
            return finder.page_links()
      
    # Takes a set of links and adds to already existing qaitlist, queue 
    def enqueue_links(self, links):
        for url in links:
            if url in Crawler.queue:
                continue
            if url in Crawler.crawled:
                continue
            # HEre, for exery link we crawl, it must belong to the site. Don't crawl the entire internet.      
            if Crawler.domain_name not in url:
                continue
            Crawler.queue.add(url)

    def update_files(self):
        set_to_file(Crawler.queue, Crawler.queue_file)
        set_to_file(Crawler.crawled, Crawler.crawled_file)
                
 
