#!/usr/bin/python

# Copyright (c) 2017 Aleksey Vitebskiy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

import argparse
import json
import sys

__all__ = ["resolve_target", "main"]

if sys.version_info.major < 3:
    from itertools import ifilter, imap
    from urllib2 import urlopen, HTTPError, URLError
    from BaseHTTPServer import BaseHTTPRequestHandler


    def indent(text, amount, ch=' '):
        padding = amount * ch
        return ''.join(padding + line for line in text.splitlines(True))
else:
    from urllib.request import urlopen, HTTPError, URLError
    from http.server import BaseHTTPRequestHandler
    from textwrap import indent

    ifilter = filter
    imap = map


def get_http_status(code):
    if code in BaseHTTPRequestHandler.responses:
        return BaseHTTPRequestHandler.responses[code][0]
    else:
        return "Unknown Response"


def resolve_target(url):
    """
    Contacts a URL and resolves the redirection target.

    :param url: The URL to resolve.
    :type url: str
    :return:" A tuple *(code, message, url)*, where *code* is the respose or error
              code, *message* is the response status or error message, and *url*
              is the resolved target URL or the input URL if no redirection was
              performed.
    :rtype: (int, string, string)
    """
    try:
        response = urlopen(url)
        return response.getcode(), get_http_status(response.getcode()), response.geturl()

    except HTTPError as err:
        return err.code, get_http_status(err.code), err.url
    except URLError as err:
        code = err.reason.errno if hasattr(err.reason, "errno") else -1
        message = err.reason.strerror if hasattr(err.reason, "strerror") else str(err.reason)
        return code, message, url
    except:
        return -1, sys.exc_info()[1], url


def print_lines(results):
    for code, message, url in results:
        print(code)
        print(message)
        print(url)
        print("")


def print_csv(results):
    for result in results:
        print('{0},"{1}","{2}"'.format(*result))


def print_json(results, pretty):
    args = {}
    endl = ""
    if pretty:
        args = {"indent": 4, "sort_keys": True, "separators": (", ", ": ")}
        endl = "\n"

    print("[", end=endl)

    i = iter(results)
    try:
        code, message, url = next(i)
        while True:
            item = json.dumps({"code": code, "message": message, "url": url}, **args)
            if pretty:
                item = indent(item, 4)
            print(item, end="")
            sys.stdout.flush()

            code, message, url = next(i)
            print(", ", end=endl)

    except StopIteration:
        pass

    print(endl + "]")


def print_results(results, format):
    if format == "lines":
        print_lines(results)
    elif format == "csv":
        print_csv(results)
    elif format == "json":
        print_json(results, False)
    elif format == "pretty-json":
        print_json(results, True)


EPILOG = '''
format options:
  lines       print the code, message, and url each on its own line. A blank line 
              separates each group of outputs
  csv         print the code, message, and url in CSV format
  json        print the code, message, and url in JSON format
  pretty-json print the code, message, and url in indented JSON format

reading URLs from a file:
  usage: resolve_target.py [-f {lines,csv,json,pretty-json}] < urls.txt
  
'''

EXAMPLES = '''
usage examples:

................................................................................

> {0} http://bit.ly/1IvcuW5                       
200
OK
http://httpbin.org/

403
Forbidden
https://www.google.com/search?q=what+is+the+answer+to+life+the+universe+and+everything

................................................................................

> {0} --format=csv http://bit.ly/1IvcuW5 https://bit.ly/2x5rRbk
200,"OK","http://httpbin.org/"
403,"Forbidden","https://www.google.com/search?q=what+is+the+answer+to+life+the+universe+and+everything"

................................................................................

> {0} --format=json http://bit.ly/1IvcuW5 https://bit.ly/2x5rRbk
[{{"url": "http://httpbin.org/", "message": "OK", "code": 200}}, {{"url": "https://www.google.com/search?q=what+is+the+answer+to+life+the+universe+and+everything", "message": "Forbidden", "code": 403}}]

................................................................................

> {0} --format=pretty-json http://bit.ly/1IvcuW5 https://bit.ly/2x5rRbk
[
    {{
        "code": 200, 
        "message": "OK", 
        "url": "http://httpbin.org/"
    }}, 
    {{
        "code": 403, 
        "message": "Forbidden", 
        "url": "https://www.google.com/search?q=what+is+the+answer+to+life+the+universe+and+everything"
    }}
]

................................................................................

> {0} invalid_url
-1
unknown url type: invalid_url
invalid_url

................................................................................

> {0} http://www.nonexistentlocation.com
-2
Name or service not known
http://www.nonexistentlocation.com

................................................................................

> {0} --format=csv < urls.txt
200,"OK","http://httpbin.org/"
403,"Forbidden","https://www.google.com/search?q=what+is+the+answer+to+life+the+universe+and+everything"

'''


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Contacts URL(s) and resolves the redirection target(s)",
        epilog=EPILOG
    )
    parser.add_argument("-e", "--examples", action="store_true",
                        help="print additional usage examples")
    parser.add_argument("urls", metavar="url", type=str, nargs="*",
                        help="the URL(s) to resolve.")
    parser.add_argument("-f", "--format", choices=["lines", "csv", "json", "pretty-json"], default="lines",
                        help="the output format (default: %(default)s)")

    args = parser.parse_args()
    if args.examples:
        print(EXAMPLES.format(parser.prog));
        parser.exit()

    urls = args.urls
    if not len(urls) and not sys.stdin.isatty():
        urls = sys.stdin.readlines()

    if not len(urls):
        parser.print_usage()
        print("No URLs were supplied", file=sys.stderr)
        parser.exit(1)

    results = imap(resolve_target, ifilter(bool, imap(str.strip, urls)))
    print_results(results, args.format)


if __name__ == "__main__":
    main()
