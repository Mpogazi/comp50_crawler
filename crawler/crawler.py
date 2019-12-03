from urllib.request import urlopen
from link_finder import LinkFinder
from util import *


class Crawler:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Crawler.project_name = project_name
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.queue_file = Crawler.project_name + '/queue.txt'
        Crawler.crawled_file = Crawler.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Crawler.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Crawler.project_name)
        create_data_files(Crawler.project_name, Crawler.base_url)
        Crawler.queue = file_to_set(Crawler.queue_file)
        Crawler.crawled = file_to_set(Crawler.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Crawler.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Crawler.queue)) + ' | Crawled  ' + str(len(Crawler.crawled)))
            Crawler.add_links_to_queue(Crawler.gather_links(page_url))
            Crawler.queue.remove(page_url)
            Crawler.crawled.add(page_url)
            Crawler.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
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

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Crawler.queue) or (url in Crawler.crawled):
                continue
            if Crawler.domain_name != get_domain_name(url):
                continue
            Crawler.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Crawler.queue, Crawler.queue_file)
        set_to_file(Crawler.crawled, Crawler.crawled_file)

    @staticmethod
    def url_list():
        return list(Crawler.crawled)
