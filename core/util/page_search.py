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


class page_search:
	"""docstring for page_search"""

	def __init__(self, framework, url, multipage, word,
				 cookie=None, agent=None, proxy=None, timeout=None):
		self.framework = framework
		self.cookie = cookie
		self.agent = agent
		self.proxy = proxy
		self.timeout = timeout
		self.url = url
		self.multipage = multipage
		self.word = word
		self._get_query = {}

	def run_crawl(self):
		search = self.framework.web_scraper(
			url=self.url,
			multipage=self.multipage,
			cookie=self.cookie,
			proxy=self.proxy,
			timeout=self.timeout,
			agent=self.agent)
		search.run_crawl()
		pages = search.get_pages
		for i in pages:
			resp = self.framework.page_parse(pages[i]).findall(self.word)
			self._get_query[i] = resp

	@property
	def get_query(self):
		return self._get_query
