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



class godork:
    """docstring for godork"""

    def __init__(self, framework, dork, limit, count, cookie,
                 agent, proxy, timeout):
        self.framework = framework
        self.cookie = cookie
        self.agent = agent
        self.proxy = proxy
        self.timeout = timeout
        self.dork = dork
        self.limit = limit
        self.count = count
        self._get_urls = []

    def run_crawl(self):
        pages = ""
        google_search = self.framework.google_engine(
            word=self.dork,
            limit=self.limit,
            count=self.count,
            cookie=self.cookie,
            agent=self.agent,
            proxy=self.proxy,
            timeout=self.timeout)
        google_search.run_crawl()
        pages = pages + google_search.get_pages
        self._get_urls = self.framework.page_parse(pages).get_sites()

    @property
    def get_urls(self):
        return self._get_urls
