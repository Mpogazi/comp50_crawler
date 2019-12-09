import sys
import threading
from queue import Queue
from crawler import Crawler
from article_finder import ArticleFinder
from util import *

def main():
    articles_queue = Queue()

    finder = ArticleFinder(1)
    finder.find_articles(articles_queue)

if __name__ == '__main__':
    main()     


