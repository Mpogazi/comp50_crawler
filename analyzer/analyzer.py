#
# given a stock and a list of links
# parses through each ilink to decide if it
# is relevant

# this class wraps the consumers in the producer-consumer
# model. The objects to be consumed are urls



import threading
import requests
import urllib.request
import re
from SafeQueue import SafeQueue
#from bs4 import BeautifulSoup

class Analyzer:

    

    def __init__(self, project_name, target_word, links_q, num_threads):
        self.target_word = target_word
        self.queue = links_q
        self.num_threads = num_threads
        self.threads = []
        self.relevant_urls = []

        self.__STOP = "~"

        # testing only
        self.project_name = project_name
        #self.test_produce()

    def start(self):
        self.threads = [threading.Thread(target = self.analyze, args = [])
                        for i in range(self.num_threads)]
        for thread in self.threads:
            thread.start()
    
    def join(self):
        for thread in self.threads:
            thread.join()    

    def analyze(self):
        url = self.queue.get()
        while url != self.__STOP:
            #try:
            req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req) as response:
                
                the_page = response.read()
               
                print(the_page)

                if re.search(self.target_word, the_page):
                    self.relevant_urls.append(url)
            #except:
                #print ("Error: Could not open ", url)

            url = self.queue.get()

        self.queue.put(self.__STOP)

    def test_produce(self):
        URLs = f.open(self.project_name + "/queue.txt")
        for url in URLs:
            url = url.rstrip()
            self.queue.put(url)

    def print_relevant_links(self):
        for url in self.relevant_urls:
            print(url)



if __name__ == '__main__':

    queue = SafeQueue()
    queue.put('https://www.iflexion.com/blog/sentiment-analysis-python')
    queue.put("~")



    a = Analyzer("test", "python", queue, 1)
    a.start()
    a.join()
    a.print_relevant_links()
