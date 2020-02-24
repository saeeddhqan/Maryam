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



class metacrawler_engine:
    """docstring for metacrawler_engine"""

    def __init__(self, framework, word, limit, count, agent, timeout, cookie, proxy):
        self.framework = framework
        self.agent = agent
        self.timeout = timeout
        self.cookie = cookie
        self.proxy = proxy
        self.word = self.framework.urlib(
            word).quote() if '%' not in word else word
        self.page = ''
        self._pages = ''
        self._links = []
        self.metacrawler = "www.metacrawler.com"
        self.count = 100 if count > 100 else count
        self.limit = 15 if limit > 15 else limit
        self.num = 1

    def searcher(self):
        url = "http://%s/serp?q=%s&page=%d" % (
            self.metacrawler, self.word, self.num)
        try:
            req = self.framework.request(
                url=url,
                cookie=self.cookie,
                agent=self.agent,
                proxy=self.proxy,
                timeout=self.timeout)
        except Exception as e:
            self.framework.error("Connection Error: " + e)
        else:
            self.page = req.text
            self._pages += self.page

    def run_crawl(self):
        while(self.num <= self.limit):
            self.searcher()
            self.num += 1

    @property
    def get_pages(self):
        return self._pages

    @property
    def get_links(self):
        self._links = self.framework.page_parse(self._pages).findall(
            r"<a class=\"web-bing__title\" href=\"([A-z0-9.,:;%/\\?#@$^&*\(\)-_+=\"\']+)\"")
        return self._links
