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

	def __init__(self, framework, q, limit=2, count=100):
		""" yahoo.com search engine

			framework : core attribute
			q 		  : query for search
			limit	  : count of pages
			count	  : count of links
		"""
		self.framework = framework
		self.q = self.framework.urlib(q).quote
		self.limit = limit
		self.count = count
		self._pages = ''
		self.yahoo = 'search.yahoo.com'

	def run_crawl(self):
		set_page = lambda x: (x*10)+1
		urls = [f'https://{self.yahoo}/search?p={self.q}&b={set_page(i)}&pz={self.count}' for i in range(1, self.limit+1)]
		max_attempt = len(urls)
		for url in range(len(urls)):
			self.framework.verbose(f"[YAHOO] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url])
			except:
				self.framework.error('[YAHOO] ConnectionError')
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Yahoo is missed!')
					break
			else:
				page = req.text
				if '">Next</a>' not in page:
					self._pages += page
					break
				self._pages += page

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		reg = r"RU=(https?%3a%2f%2f[^/]+)/"
		tmp = self.framework.page_parse(self._pages).findall(reg)
		links = []
		for link in tmp:
			link = self.framework.urlib(link).unquote
			links.append(link)
		return links
	
	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
