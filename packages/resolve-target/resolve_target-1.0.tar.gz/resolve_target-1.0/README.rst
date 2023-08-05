resolve\_target
===============

Contacts URL(s) and resolves the redirection target(s).

Summary
-------

This utility takes a list of URLs from either command line arguments or
a file. It sends an HTTP GET request to each URL, follows any redirect
responses, and outputs the actual target URL. The output includes the
response code, the status message, and the target URL.

If a URL is invalid, the response code and response status is replaced
with an error code (if applicable) and the error message. The input URL
will be echoed in the output in this case.

Command Line Usage
------------------

``resolve_target [-h] [-e] [-f {lines,csv,json,pretty-json}] [url [url ...]]``

Positional Arguments
~~~~~~~~~~~~~~~~~~~~

-  ``url`` - The URL(s) to resolve. Multiple URLs can be listed.

Optional Arguments
~~~~~~~~~~~~~~~~~~

-  ``-h``, ``--help`` - Shows the help message and exits.
-  ``-e``, ``--examples`` - Prints additional usage examples.
-  ``-f``, ``--format`` - Sets the output format. The valid values are
   ``lines``, ``csv``, ``json``, ``pretty-json``. The default value is
   ``lines``.

Format Options
~~~~~~~~~~~~~~

The utility can format its output in several formats. The formats
include CSV, JSON, and simply printing each item on its own line, with
records separated by an extra blank line.

lines
^^^^^

The ``lines`` option prints the code, message, and URL each on its own
line. A blank line separates each group of inputs.

Example
'''''''

::

    > resolve_target --format=lines http://bit.ly/1IvcuW5 https://bit.ly/2x5rRbk
    200
    OK
    http://httpbin.org/

    403
    Forbidden
    https://www.google.com/search?q=what+is+the+answer+to+life+the+universe+and+everything

csv
^^^

The ``csv`` option prints the code, message, and url in CSV format, one
line per URL.

Example
'''''''

::

    > resolve_target --format=csv http://bit.ly/1IvcuW5 https://bit.ly/2x5rRbk
    200,"OK","http://httpbin.org/"
    403,"Forbidden","https://www.google.com/search?q=what+is+the+answer+to+life+the+universe+and+everything"

json
^^^^

The ``json`` option prints the code, message, and URL in JSON format
without formatting.

Example
'''''''

::

    > resolve_target --format=json http://bit.ly/1IvcuW5 https://bit.ly/2x5rRbk
    [{"url": "http://httpbin.org/", "message": "OK", "code": 200}, {"url": "https://www.google.com/search?q=what+is+the+answer+to+life+the+universe+and+everything", "message": "Forbidden", "code": 403}]

pretty-json
^^^^^^^^^^^

::

    > resolve_target --format=pretty-json http://bit.ly/1IvcuW5 https://bit.ly/2x5rRbk
    [
        {
            "code": 200, 
            "message": "OK", 
            "url": "http://httpbin.org/"
        }, 
        {
            "code": 403, 
            "message": "Forbidden", 
            "url": "https://www.google.com/search?q=what+is+the+answer+to+life+the+universe+and+everything"
        }
    ]

Reading URLs From a File
~~~~~~~~~~~~~~~~~~~~~~~~

If a text file is redirected into the ``resolve_target`` utility,
``resolve_target`` will read the URLs from that file. The file should
have the URLs listed one per line.

Example
^^^^^^^

Contents of **urls.txt**:

::

    http://bit.ly/1IvcuW5
    https://bit.ly/2x5rRbk

Usage:

::

    > resolve_target --format=pretty-json < urls.txt                                  
    [
        {
            "code": 200, 
            "message": "OK", 
            "url": "http://httpbin.org/"
        }, 
        {
            "code": 403, 
            "message": "Forbidden", 
            "url": "https://www.google.com/search?q=what+is+the+answer+to+life+the+universe+and+everything"
        }
    ]

Non-HTTP Errors
~~~~~~~~~~~~~~~

If a URL could not be reached, ``resolve_target`` will output the error
code (if applicable), the error message, and the requested URL. If
there's no relevant error code, the error code will be set to -1.

Examples
^^^^^^^^

::

    > resolve_target invalid_url
    -1
    unknown url type: invalid_url
    invalid_url

``> resolve_target http://www.nonexistentlocation.com -2 Name or service not known http://www.nonexistentlocation.com``
