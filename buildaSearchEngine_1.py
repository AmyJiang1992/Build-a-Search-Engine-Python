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
# In order to do this, we need to think about two things.
# First, keep track of all pages that we're waiting to crawl

# @tocrawl: a list of pages left to crawl. Initially, the seed page.
# @crawled: a list of pages crawled. Initially, empty list, [].

# pseudo code:
start with tocrawl = [seed]
crawled = []
while there are more pages to crawl:
    pick a page from tocrawl
    add that page to crawled
    add all the link targets on this page to tocrawl
return crawled

# HOWEVER, if we follow this process on the given test site, with the seed page, it will never return.
# The crawler will never finish because it will always find a link to crawl.
# Example: page A has link to page B, and page B has link to page A, the two pages links to each other again and again.
# TO avoid this, we need to do something smarter. We need to make sure that we don't crawl pages that we already done.
# update pseudo code:
start with tocrawl = [seed]
crawled = []
while there are more pages to crawl:
    pick a page from tocrawl
    check if we already crawled it!
    add that page to crawled
    add all the link targets on this page to tocrawl
return crawled    
# Now we are going to define a procedure crawl_web that takes as input a seed page url, and 
# output a list of all urls that can be reached by following links starting from the seed page.
def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            union(tocrawl, get_all_links(get_page(page)))
            crawled.append(page)
    return crawled
# Procedure get_page is a given procedure transfer url to html. A procudure which actually grabs a page from the web
# will be talked about later.

# The web crawler we built has some serious flaws if we were going to use it in a real crawler. 
# One problem is if we start with a good seed page, it might run for an extremely long time (even forever, since the
# number of URLS on the web is not actually finite). 
# Now we are going to explore two different ways to limit the pages that it can crawl.

# The first way:
# Modify the crawl_web procedure to take a second parameter, max_pages, that limits the number of pages to crawl.
# We expect the procedure terminate the crawl after max_pages different pages have been crawled,
# or when there are no more pages to crawl.
# Here is updated crawl_web procedure:
def crawl_web(seed, max_pages):
    tocrawl = [seed]
    crawled = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled and len(crawled) < max_pages:
            union(tocrawl, get_all_links(get_page(page)))
            crawled.append(page)
    return crawled
# The second way:
# Modify the crawl_web procedure to take a second parameter, max_depth, that limits the depth of the search.  
# We can define the depth of a page as the number of links that must be followed to reach that page starting from the seed page,
# that is, the length of the shortest path from the seed to the page.  
# No pages whose depth exceeds max_depth should be included in the crawl.  
# For example
# If max_depth is 0, the only page that should be crawled is the seed page. 
# If max_depth is 1, the pages that should be crawled are the seed page and every page that it links to directly. 
# If max_depth is 2, the crawl should also include all pages that are linked to by these pages.
# Here is updated crawl_web procedure:
def crawl_web(seed,max_depth):    
    tocrawl = [seed]
    crawled = []
    next_depth = []# Keep track of next level of links
    depth = 0
    while tocrawl and depth <= max_depth:
        page = tocrawl.pop()
        if page not in crawled:
            union(next_depth, get_all_links(get_page(page)))
            crawled.append(page)
        if not tocrawl:
        # When tocrawl is empty, it means this level is all crawled and ready to craw next level
            tocrawl, next_depth = next_depth, []
            depth = depth + 1
    return crawled


