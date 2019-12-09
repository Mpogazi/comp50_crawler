'''
ANALYZER

Description:
    Given a list of stock names and a queue of article urls, the Analyzer
    spawns multiple threads to read through the contents of each article and
    decide if they contain a target stock name. Then, it updates the database
    at the given url.


Synchronization:
    Queue: This class uses a synchronized Queue from the python queue module
           The analyzer spawns multiple threads that act as consumers in a
           producer-consumer relationship with the Crawler class.
    Locks: Multile threads will be accessing and updating the same dictionary,
           so to prevent two threads from changing something at the same index,
           we've made a second dictionary that holds locks for each item in the
           main dictionary.
'''


import threading
import queue
import sys


from bs4 import BeautifulSoup
import urllib.request
import requests

import time


class Analyzer:

    STOP = "ANALYZER_STOP"

    def __init__(self, target_words, links_q, num_threads, DB_url = ""):
        self.target_words = target_words
        self.queue = links_q
        self.num_threads = num_threads
        self.threads = []


        # parallel dictionaries
        self.relevant_articles = {i:{"name": i, "update": []} for i in target_words}
        self.stock_locks = {i:threading.Lock() for i in target_words}

        self.DB_URL = DB_url
        self.company_words = ["Inc.", "LLC", "Corp.", "Co."]


    def start(self):
        self.threads = [threading.Thread(target = self.analyze, args = [])
                        for i in range(self.num_threads)]
        for thread in self.threads:
            thread.start()

    def join(self):
        for thread in self.threads:
            thread.join()

        self.update_db()

    def update_db(self):
        if not self.DB_URL == "":
            for stock in self.relevant_articles.keys():
                requests.post(self.DB_URL, data = self.relevant_articles[stock])
        return

    def analyze(self):
        url = self.queue.get(True, 10)
        while url != Analyzer.STOP:

            try:
                source = urllib.request.urlopen(url)
                soup = BeautifulSoup(source, 'html.parser')
            except:
                sys.stderr.write(threading.current_thread().name +
                                 " --- Error: Could not open " + url)
                url = self.queue.get(True, 10)
                continue

            for stock in self.target_words:
                to_search = self.clean_stock(stock)
                if to_search in soup.title.text:
                    with self.stock_locks[stock]:
                        self.relevant_articles[stock]["update"].append(
                        {"article_title":soup.title.text,
                         "article_url": url})
                else:
                    paragraphs = soup.find_all('p')
                    for p in paragraphs:
                        if to_search in p.text:
                            with self.stock_locks[stock]:
                                self.relevant_articles[stock]["update"].append(
                                {"article_title":soup.title.text,
                                 "article_url": url})
                            break
            url = self.queue.get(True, 10)

        self.queue.put(Analyzer.STOP)


    def clean_stock(self, stock_name):
        for c_word in self.company_words:
            if c_word in stock_name:
                stock_name = " ".join(stock_name.split()[:-1])
        return stock_name



# **********************  Testing Only  *******************************

    def test_produce(self):
        # f = open("testQueue.txt")
        # for url in f:
        #     self.queue.put(url)
        # f.close()
        for i in range(20):
            self.queue.put("https://www.thestreet.com/investing/amazon-"
            + "new-york-city-expansion")
        self.queue.put(Analyzer.STOP)



    def print_relevant_articles(self):
        for stock in self.relevant_articles.keys():
            print(stock)
            for article in self.relevant_articles[stock]["update"]:
                print(article["article_title"])
                print(article["article_url"])
                print()
            print("\n")


# Testing only
if __name__ == '__main__':

    queue = queue.Queue()
    a = Analyzer(["Apple Inc.", "Microsoft Inc.",
           "Amazon Co.", "TD", "Tesla", "Google LLC."], queue, 15, "")
    a.test_produce()
    start_time = time.time()
    a.start()
    a.join()
    #a.print_relevant_articles()
    print(time.time() - start_time)
