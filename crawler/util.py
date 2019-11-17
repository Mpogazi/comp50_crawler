import os
from urllib.parse import urlparse

# Each website crawled is a separate proj. links go in directory
def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating directory " + directory)
        os.makedirs(directory)

# Create queue and crawled files
# base_url is starting point
def create_data_files(project_name, base_url):
    queue   = project_name + "/queue.txt"
    crawled = project_name + "/crawled.txt"
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')
   
# Create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close() 

# Append data to existing file - new link
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

# Delete contents of file
def delete_file_contents(path):
    with open(path, 'w'):
        pass

# Read a file and convert each line to set item
def file_to_set(fname):
    results = set()
    with open(fname, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

#Iterate through set and write links to files
def set_to_file(links, path):
    delete_file_contents(path)
    for link in sorted(links):
        append_to_file(path, link) 

# get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''

# get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


