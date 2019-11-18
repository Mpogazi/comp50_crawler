from html.parser import HTMLParser
from urllib import parse

# The Link Finder class, parses HTML for links and compiles them in a set.

class LinkFinder(HTMLParser):
       
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, val) in attrs: 
                if attribute == "href":
                    # if we come across absolute url we can just add it 
                    # but we need to convert relative urls to full urls 
                    url = parse.urljoin(self.base_url, val)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass
