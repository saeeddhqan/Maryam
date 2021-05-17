"""
OWASP Maryam!

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

import re


class main:

    def __init__(self, q, limit=1):
        """
        darksearch.io search engine

        q          : Query for search
        limit      : Number of pages
        """

        self.framework = main.framework
        self.q = q
        self._pages = ''
        self.limit = limit
        self._links = []
        self._json = []
        self.darksearch = 'darksearch.io'
        self._json_links = []

    def run_crawl(self):
        urls = [f"https://{self.darksearch}/api/search?query={self.q}&page={i}" for i in range(1, self.limit+1)]
        max_attempt = len(urls)
        for url in range(max_attempt):
            self.framework.verbose(f"[DARKSEARCH] Searching in {url} page...")
            try:
                req = self.framework.request(url=urls[url], allow_redirects=True)
            except Exception as e:
                self.framework.error('ConnectionError', 'util/darksearch', 'run_crawl')
                max_attempt -= 1
                if max_attempt == 0:
                    self.framework.error('Darksearch is missed!', 'util/darksearch', 'run_crawl')
                    break

            if req.json()['data'] is None:
                break
            self._pages += req.text
            self._json.append(req.json())

    @property
    def pages(self):
        return self._pages

    @property
    def json(self):
        return self._json

    @property
    def links(self):
        for page in self.json:
            results = page.get('data', {})
            if not results:
                return {}
            self._links.extend(x.get('link') for x in results)
        return self._links

    @property
    def json_links(self):
        for page in self.json:
            results = page.get('data', {})
            if not results:
                return {}
            self._json_links.extend(results)
        return self._json_links
