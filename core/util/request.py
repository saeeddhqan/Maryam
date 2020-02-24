#! /usr/bin/python
# -*- coding: u8 -*-
"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Request v2.3

import gzip
import json
import socket
import ssl
from codecs import utf_8_encode, utf_8_decode
from base64 import b64encode
try:
    from StringIO import StringIO
    import urllib2 as request
    from urllib import urlencode
except (NameError, ImportError):
    from io import StringIO
    from urllib import request
    from urllib.parse import urlencode

# create a global ssl context that ignores certificate validation
if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context


def encode_payload(in_dict):
    out_dict = {}
    for i in in_dict:
        v = in_dict[i]
        if isinstance(v, bytes):
            v = utf_8_encode(v)
        elif isinstance(v, str):
            # must be encoded in UTF-8
            v = utf_8_decode(v)
        out_dict[i] = v
    return out_dict


class req(object):
    """docstring for req"""

    def __init__(self, framework, **kwargs):
        '''Initializes control parameters as class attributes.'''
        self.framework = framework
        self.user_agent = "Maryam.request/v2.3" if "user_agent" not in kwargs else kwargs["user_agent"]
        self.debug = False if "debug" not in kwargs else kwargs["debug"]
        self.proxy = None if "proxy" not in kwargs else kwargs["proxy"]
        self.timeout = None if "timeout" not in kwargs else kwargs["timeout"]
        self.redirect = True if "redirect" not in kwargs else kwargs["redirect"]

    def send(self, url, method="GET", payload=None,
             headers=None, cookie=None, auth=None, content=''):

        # initialize url service
        urlib = self.framework.urlib(url)
        if(urlib.get_scheme == ''):
            url = urlib.sub_service("http")

        # Makes a web request and returns a response object.
        if method.upper() != "POST" and content:
            raise RequestException(
                "Invalid content type for the %s method: %s" %
                (method, content))
        # prime local mutable variables to prevent persistence
        if payload is None:
            payload = {}
        if headers is None:
            headers = {}
        if auth is None:
            auth = ()

        # set request arguments
        # process user-agent header
        headers["User-Agent"] = self.user_agent
        if(headers["User-Agent"] is None):
            headers["User-Agent"] = self.user_agent
        # process payload
        if content.upper() == "JSON":
            headers["Content-Type"] = "application/json"
            payload = json.dumps(payload)
        else:
            payload = urlencode(encode_payload(payload))
        # process basic authentication
        if len(auth) == 2:
            authorization = b64encode(utf_8_encode(
                '%s:%s' % (auth[0], auth[1]))).replace('\n', '')
            headers["Authorization"] = "Basic %s" % (authorization)
        # process socket timeout
        if self.timeout:
            socket.setdefaulttimeout(self.timeout)

        # set handlers
        # declare handlers list according to debug setting
        handlers = [
            request.HTTPHandler(
                debuglevel=1), request.HTTPSHandler(
                debuglevel=1)] if self.debug else []
        # process cookie handler
        if cookie is not None and cookie != {}:
            if isinstance(cookie, dict):
                str_cookie = ""
                for i in cookie:
                    str_cookie += "%s=%s; " % (i, cookie[i])
                headers["Cookie"] = str_cookie
            else:
                handlers.append(request.HTTPCookieProcessor(cookie))

        # process redirect and add handler
        if not self.redirect:
            handlers.append(NoRedirectHandler)
        # process proxies and add handler
        if self.proxy:
            proxies = {"http": self.proxy, "https": self.proxy}
            handlers.append(request.ProxyHandler(proxies))

        # install opener
        opener = request.build_opener(*handlers)
        request.install_opener(opener)
        # process method and make request
        if method == "GET":
            if payload:
                url = "%s?%s" % (url, payload)
            req = request.Request(url, headers=headers)
        elif method == "POST":
            req = request.Request(url, data=payload, headers=headers)
        elif method == "HEAD":
            if payload:
                url = "%s?%s" % (url, payload)
            req = request.Request(url, headers=headers)
            req.get_method = lambda: "HEAD"
        else:
            raise RequestException(
                "Request method \'%s\' is not a supported method." %
                (method))

        try:
            resp = request.urlopen(req)
        except request.HTTPError as e:
            resp = e

        # build and return response object
        return ResponseObject(resp, cookie)


class NoRedirectHandler(request.HTTPRedirectHandler):

    def http_error_302(self, req, fp, code, msg, headers):
        pass

    http_error_301 = http_error_303 = http_error_307 = http_error_302


class ResponseObject(object):

    def __init__(self, resp, cookie):
        self.resp = resp
        # set raw response property
        self.raw = resp.read()
        # set inherited properties
        self.url = resp.geturl()
        self.status_code = resp.getcode()
        # detect and set encoding property
        self.headers = dict(resp.headers)
        try:
            self.encoding = resp.headers.getparam("charset")
            self.content_type = resp.headers.getparam("content-type")
            self.content_encoding = resp.headers.getparam("content-encoding")
        except AttributeError:
            self.encoding = resp.headers.get_param("charset")
            self.content_type = resp.headers.get_param("content-type")
            self.content_encoding = resp.headers.get_param("content-encoding")
        self.cookie = cookie
        # deflate payload if needed
        if self.content_encoding == "gzip":
            self.deflate()
        resp.close()

    def deflate(self):
        with gzip.GzipFile(fileobj=StringIO(self.raw)) as gz:
            self.raw = gz.read()

    @property
    def text(self):
        try:
            return self.raw.decode(self.encoding)
        except (UnicodeDecodeError, TypeError):
            text = ""
            for i in range(len(self.raw)):
                char = str(self.raw[i])
                if(char[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                    char = chr(int(char))
                if(ord(char) in [9, 10, 13] + list(range(32, 126))):
                    text += char
            return text

    @property
    def json(self):
        try:
            return json.loads(self.text)
        except ValueError:
            return None

    @property
    def read(self):
        return self.raw


class RequestException(Exception):
    pass
