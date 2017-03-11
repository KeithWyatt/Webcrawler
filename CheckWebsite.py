#! /opt/bin/python3
#Keith Wyatt
# Creating a web Crawler for broken links
# June 27 2015

import urllib.request
import urllib.error
import argparse
import re
import sys


timeout = 1         # 1 second limit on reading a webpage
maxlength = 10000   # max number of bytes to read from a webpage
maxhits = 100       # max number of URLs we will try to open
hits = 0            # number of URL open attempts

def readwebpage( url ):
    """Reads the contents of a webpage at the given URL and returns
       the contents of that webpage as a string.
       If the maximum number of URL accesses has been reached (set by
       the value of the global variable maxhits), the webpage is not
       read and the result is an empty string.
       If the URL causes a HTTP error (usually error 404 page not found),
       the result is the value None.
       If any other kind of error is caught, the result is a short string
       which contains the URL and says there was an error."""
    global hits, maxhits, timeout, maxlength,error_pages
    if hits >= maxhits:
        return ""
    hits += 1
    try:
        with urllib.request.urlopen(url, None, timeout) as response:
            bytes = response.read(maxlength)
            return bytes.decode("utf-8")
    except urllib.error.HTTPError:
        print("Error at page", url)
        error_pages = error_pages +1
        return None     # a 404 HTTP error or similar
    except urllib.error.URLError:
        return None     # a 404 HTTP error or similar
    except:
        # it's some other kind of error
        error_pages = error_pages +1
        return "Error with URL: "+url


def main():
    global maxhits,error_pages
    parser = argparse.ArgumentParser(description="Check a website.")
    parser.add_argument('-maxvisits', dest='maxhits', type=int, default=10,
        help="limit the number of url's which will be tested")
    parser.add_argument('url', metavar='url', type=str, nargs=1,
        help='the URL of a website')

    args = parser.parse_args()
    maxhits = args.maxhits
    url = args.url[0]

    url_list = [url]
    been_to_urls = [url]
    number_of_visits = 0
    s = readwebpage(url)
    error_pages = 0
    checked_sites = 0
    url_list = set(url_list)
    test = url
    dictionary_webs = {}

    if(maxhits <0):
        print ("The number of site to visit must be more than zero")
        sys.exit(0)
    elif(maxhits ==0):
        print( "Zero webpages were visited")
        sys.exit(0)
    elif(maxhits >100):
        print("Can only visit webpages 100, otherwise it's a DDoS attack")
        maxhits = 100
    else:
        print ("Maximum number of webpage visits set to ", maxhits)

    #checking to see if we've been to the website too many times
    while (url_list and number_of_visits < maxhits and number_of_visits < 100):
        checked_sites = checked_sites + 1
        url_parent = url
        last_url = url_parent
        url = url_list.pop()
        test = readwebpage(url)
        number_of_visits = number_of_visits + 1

        if test == None:
            dictionary_webs[url_parent] = url
            print ("bad reference to ", url)
            error_pages = error_pages +1
        else:
            urls_listings = re.findall(r'href="([\s:]?[^\'">]+)',test)
            duplicate = urls_listings[:]
            dictionary_webs[url] = []
            while duplicate:
                dictionary_webs[url].append(duplicate.pop())
            while urls_listings:
                website = urls_listings.pop()
                while (website in been_to_urls and urls_listings):
                    website = urls_listings.pop()
                while (website in url_list and urls_listings):
                    website = urls_listings.pop
                if urls_listings:
                    url_list.add(website)
                    been_to_urls.append(website)

    print("checking finished ",checked_sites, "Webpages errors checked", error_pages)


if __name__ == "__main__":
    main()


