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

import hashlib
import re
import urllib


class netcraft_search:

    def __init__(self, framework, word, agent, proxy, timeout):
        self.word = word
        self.framework = framework
        self.server = 'netcraft.com'
        self.agent = agent
        self.timeout = timeout
        self.proxy = proxy
        self.base_url = 'https://searchdns.netcraft.com/?restriction=site+ends+with&host=' + word
        self.timeout = timeout if timeout else 25
        self._pages = ""

    def request(self, url, cookies=None):
        cookies = cookies or {}
        try:
            req = self.framework.request(
                url=url,
                cookie=cookies,
                agent=self.agent,
                proxy=self.proxy,
                timeout=self.timeout)
        except Exception as e:
            self.framework.error(e)
            req = None
        else:
            return req

    def get_next(self, resp):
        link_regx = re.compile('<A href="(.*?)"><b>Next page</b></a>')
        link = link_regx.findall(resp)[0]
        url = 'https://searchdns.netcraft.com' + link.replace(" ", "%20")
        return url

    def get_cookies(self, headers):
        if 'set-cookie' in headers:
            cookie = headers['set-cookie']
            cookies = {}
            cookies_list = cookie[0:cookie.find(';')].split("=")
            cookies[cookies_list[0]] = cookies_list[1]
            # get js verification response
            cookies['netcraft_js_verification_response'] = hashlib.sha1(
                urllib.unquote(cookies_list[1]).encode('utf-8')).hexdigest()
        else:
            cookies = {}
        return cookies

    def run_crawl(self):
        start_url = self.base_url
        resp = self.request(start_url)
        cookies = self.get_cookies(resp.headers)
        while True:
            resp = self.request(self.base_url, cookies).text
            self._pages += resp
            if 'Next page' not in resp or resp is None:
                break
            self.base_url = self.get_next(resp)

    def get_dns(self):
        resp = []
        find = re.findall(r"[A-z0-9\.\-]+\.%s" % self.word, str(self._pages))
        for i in find:
            if i not in resp:
                resp.append(i)
        return resp
