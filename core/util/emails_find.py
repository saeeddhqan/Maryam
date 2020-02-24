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



class emails_find:
    """docstring for email_find"""

    def __init__(
            self,
            framework,
            company,
            limit,
            count,
            engines,
            cookie=None,
            agent=None,
            proxy=None,
            timeout=None):
        self.framework = framework
        self.cookie = cookie
        self.agent = agent
        self.proxy = proxy
        self.timeout = timeout
        self.company = company
        self.limit = limit
        self.count = count
        self.engines = engines
        self._engines = ["bing", "google", "yahoo", "yandex", "metacrawler", "ask"]
        self._get_emails = []

    def run_crawl(self):
        pages = ""
        alert_mode = self.framework._global_options["verbosity"] == 2
        for i in self.engines:
            if(i.lower() in self._engines):
                if(alert_mode):
                    self.framework.alert("Search in \"%s\"" % i)
                try:
                    attr = getattr(self.framework, "%s_engine" % i)(
                        word="%40" + self.company,
                        limit=self.limit,
                        count=self.count,
                        cookie=self.cookie,
                        agent=self.agent,
                        proxy=self.proxy,
                        timeout=self.timeout)
                    attr.run_crawl()
                except Exception as e:
                    self.framework.error("Connection Error: " + e.message)
                else:
                    pages = pages + attr.get_pages
            else:
                if(alert_mode):
                    self.framework.error(
                        "Search Engine \"%s\" Not Found !" % i)

        self._get_emails = self.framework.page_parse(
            pages).get_emails(self.company)

    @property
    def get_emails(self):
        return self._get_emails
