#!/usr/bin/env python3
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

class main:

	def __init__(self, q, limit=10):
		""" keyserver.ubuntu.com search engine

			q 		  : query for search
			limit	  : Number of pages
		"""
		self.framework = main.framework
		self.q = q
		self.limit = limit
		self._pages = ''
		self._json_pages = ''
		self.keyserver_api = f"https://keyserver.ubuntu.com/pks/lookup?search=@{self.q}&op=index"
		self.acceptable = False

	def run_crawl(self):
		self.framework.verbose('[KEYSERVER] Searching in keyserver...')
		try:
			req = self.framework.request(self.keyserver_api)
		except:
			self.framework.debug('ConnectionError', 'util/keyserver', 'run_crawl')
			self.framework.error('Keyserver is missed!', 'util/keyserver', 'run_crawl')
			return
		self._pages += req.text
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def pages(self):
		return self._pages
	
	@property
	def json_pages(self):
		return self._json_pages

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def dns(self):
		return self.framework.page_parse(self.pages).get_dns(self.q)

