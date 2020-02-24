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



class reverse_ip:
    """docstring for reverse_ip"""

    def __init__(self, framework, nameserver, limit, count, cookie=None,
                 agent=None, proxy=None, timeout=None):
        self.framework = framework
        self.limit = limit
        self.cookie = cookie
        self.agent = agent
        self.proxy = proxy
        self.timeout = timeout
        self.nameserver = nameserver
        self.limit = limit
        self.count = count
        self._get_domains = []

    def run_crawl(self):
        server = self.nameserver
        server = self.framework.urlib(server).get_ip
        try:
            bing = self.framework.bing_engine(
                word="ip%3A" + server,
                limit=self.limit,
                count=self.count,
                cookie=self.cookie,
                agent=self.agent,
                proxy=self.proxy,
                timeout=self.timeout)
            bing.run_crawl()
        except Exception as e:
            self.framework.error("Connection Error: " + e.message)
        else:
            resp = bing.get_pages
            self._get_domains = self.framework.page_parse(resp).get_sites()

    @property
    def get_domains(self):
        return self._get_domains
