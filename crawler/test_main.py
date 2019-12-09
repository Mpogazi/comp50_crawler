import sys
import threading
from queue import Queue
from crawler import Crawler
from article_finder import ArticleFinder
from util import *

def main():
    articles= Queue()

    finder = ArticleFinder(2)
    finder.find_articles(articles)

    articles_file = open("articles.txt", "w")
    for article in articles.queue:
        articles_file.write(article)
        articles_file.write("\n")

    articles_file.close()        


if __name__ == '__main__':
    main()     


