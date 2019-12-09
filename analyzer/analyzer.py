'''
ANALYZER

Description:
    This class


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




class Analyzer:

    STOP = "~"

    def __init__(self, target_words, links_q, num_threads, DB_url):
        self.target_words = target_words
        self.queue = links_q
        self.num_threads = num_threads
        self.threads = []

        # parallel dictionaries
        self.relevant_articles = {i:[] for i in target_words}
        self.stock_locks = {i:threading.Lock() for i in target_words}

        self.DB_URL = DB_url


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
            requests.post(self.DB_URL, data = self.relevant_articles)
        return

    def analyze(self):
        url = self.queue.get(True, 10)
        while url != Analyzer.STOP:

            try:
                source = urllib.request.urlopen(url)
                soup = BeautifulSoup(source, 'html.parser')
            except:
                sys.stderr.write(threading.current_thread().name + " --- Error: Could not open " + url)
                url = self.queue.get(True, 10)
                continue


            for stock in self.target_words:
                if stock in soup.title.text:
                    with self.stock_locks[stock]:
                        self.relevant_articles[stock].append((soup.title.text, url))
                else:
                    links = soup.find_all('p')
                    for p in links:
                        if stock in p.text.split():
                            with self.stock_locks[stock]:
                                self.relevant_articles[stock].append((soup.title.text, url))
                            break
            url = self.queue.get(True, 10)

        self.queue.put(Analyzer.STOP)




# **********************  Testing Only  *******************************

    def test_produce(self):
        f = open("analyzer/testQueue.txt")
        for url in f:
            self.queue.put(url)
        f.close()
        self.queue.put(Analyzer.STOP)



    def print_relevant_articles(self):
        for stock in self.relevant_articles.keys():
            print(stock)
            for article in self.relevant_articles[stock]:
                print(article[0])
                print(article[1])
                print()
            print("\n")


    def get_relevant_articles(self):
        data = {}
        data['articles'] = self.relevant_articles
        return json.dumps(data)


if __name__ == '__main__':

    queue = queue.Queue()

    a = Analyzer(["United", "Apple", "Microsoft", "Amazon", "TD", "Tesla"], queue, 10, "")
    a.test_produce()
    a.start()
    a.join()
    a.print_relevant_articles()
