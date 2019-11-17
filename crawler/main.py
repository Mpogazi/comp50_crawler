import sys
import threading
from queue import Queue
from crawler import Crawler
from util import *

# CL iknterface, for one given base_url, gathers all URLs on that page and
# saves to disc

#Handle arguments
def get_args():
    if len(sys.argv) is not 3:
        print("Incorrect arguments")
        sys.exit(1)
    else:
        args = []
        for arg in sys.argv[1:]:
            args.append(arg)
 
    return args

def main():
    project_name, homepage = get_args()
    domain_name  = get_domain_name(homepage)
    queue_file   = project_name + "/queue.txt"
    crawled_file = project_name + "/crawled.txt"
    Crawler(project_name, homepage, domain_name)


if __name__ == '__main__':
    main()     
