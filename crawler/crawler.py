from urllib.request import urlopen
from crawler.link_finder import LinkFinder
from queue import Queue
from crawler.util import *

class Crawler:

    base_url = ''
    domain_name = ''
    article_dir = ''    
    articles_file = ''
    to_be_crawled = set()
    crawled       = set()

    def __init__(self, publication, base_url, domain_name, article_dir, articles_queue):
        print("New Crawler Crawling: " + publication)
        self.print_urlsets()
        Crawler.base_url      = base_url
        Crawler.domain_name   = domain_name
        Crawler.article_dir   = article_dir
        Crawler.articles_file = 'articles.txt'
        Crawler.to_be_crawled.clear()
        Crawler.crawled.clear() 
        Crawler.to_be_crawled.add(Crawler.base_url)
        self.crawl_page(Crawler.base_url, articles_queue)

    # Populate to_be_crawled with links found in HTML of page_url
    # If link article, also add to shared articles queue
    @staticmethod
    def crawl_page(page_url, articles_queue):
        if page_url not in Crawler.crawled:
            print('| Queue ' + str(len(Crawler.to_be_crawled)) + ' | Crawled  ' + str(len(Crawler.crawled)))
            Crawler.add_links_to_be_crawled(Crawler.gather_links(page_url))
            Crawler.to_be_crawled.remove(page_url)
            if Crawler.article_dir  in page_url:                
                articles_queue.put(page_url)
            Crawler.crawled.add(page_url)

    # Check good html formatting
    # Return all urls found on page as set of links
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Crawler.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Add links to to_be_crawled if correct domain and not crawled or in to_be_crawled
    @staticmethod
    def add_links_to_be_crawled(links):
        for url in links:
            if (url in Crawler.to_be_crawled) or (url in Crawler.crawled):
                continue
            if Crawler.domain_name != get_domain_name(url):
                continue
            Crawler.to_be_crawled.add(url)

    @staticmethod
    def reset_urlsets():
        Crawler.to_be_crawled.clear()
        Crawler.crawled.clear()

    @staticmethod
    def print_urlsets():
        print(Crawler.to_be_crawled)
        print(Crawler.crawled)

