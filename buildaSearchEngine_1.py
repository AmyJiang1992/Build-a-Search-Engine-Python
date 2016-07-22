# To realize a search engine. We need to first realize extracting a link from its page.
# Before get to the code, I want to describe a little more carefully what's going on in a web page.
# All a web page really is a long string! When we see a web page in brower, it doesn't seem like that. 
# But when you right click on the page, View Page Source, you can see actual source code.
# We focus on the links. 
# Example: 
#        <li><a href="/archive/">Archive</a><br /></li>
# HTML uses angle brackets and the angle bracket "a href=" is how we start a link.
# The following string which is surrounded by double quotes is a URL.
# Not all webpages have the same structure. There're lots of ways to make a tag.
# But in this project, we assume all our webpages follows the same strucure.
# So we simplified the problem of finding out links in a webpage into extracting substrings from a long string.
# Get URL from ..........<a href="<URL>">.................
# 
# Here is the simplest procedure to get an URL.

def get_next_target(page):
    start_link = page.find('<a href=')
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote
  
# Modify the get_next_target procedure so that if there is a link it behaves as before
# But if the input doesn't contain any link, it outputs None, 0.

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote
    
# We define a procedure, print_all_links, to print on screen all links we got from that page.
def print_all_links(page):
    while True:
        url, endpos = get_next_target(page)
        if url:
            print url
            page = page[endpos:]
        else:
            break
            
# We now decide to not print all links but get all links.
# And instead of outputing None, we output a list of links.
def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links
    
# We define a procudure, union, that takes as inputs 2 lists.
# It should modify the first input list to be the set union of the 2 lists.
# That is add all the elements in the second list to the first list, except if they already exist. No duplicate.
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
            
# Now we are ready to finish the web crawler.
# What a  web crawler do is: we have a seed page with some links on it. We want to be able to find those links.
# We get them to list and then we follow them to new pages. New pages might also have links and we want to follow those links.
# In order to do this, we need to think about to things.
# First, keep track of all pages that we're waiting to crawl

# @tocrawl: a list of pages left to crawl. Initially, the seed page


