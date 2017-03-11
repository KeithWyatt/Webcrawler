#! /opt/bin/python3
# Read and print the HTML code for a webpage
#
# Example of usage:
#    python3 VisitURL.py http://foo.bar.ca

import urllib.request
import urllib.error
import argparse

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
    global hits, maxhits, timeout, maxlength
    if hits >= maxhits:
        return ""
    hits += 1
    try:
        with urllib.request.urlopen(url, None, timeout) as response:
            bytes = response.read(maxlength)
            return bytes.decode("utf-8")
    except urllib.error.HTTPError:
        return None     # a 404 HTTP error or similar
    except urllib.error.URLError:
        return None     # a 404 HTTP error or similar
    except:
        # it's some other kind of error
        return "Error with URL: "+url

def main():
    global maxhits
    parser = argparse.ArgumentParser(description="Check a website.")
    parser.add_argument('-maxvisits', dest='maxhits', type=int, default=10,
        help="limit the number of url's which will be tested")
    parser.add_argument('url', metavar='url', type=str, nargs=1,
        help='the URL of a website')
    
    args = parser.parse_args()
    maxhits = args.maxhits
    url = args.url[0]

    s = readwebpage(url)
    if s:
        print("Website contents are:")
        print(s)
    else:
        print("Website could not be read")

if __name__ == "__main__":
    main()