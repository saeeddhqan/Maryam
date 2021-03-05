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
import os

class main:

	def __init__(self, framework, q, key, limit=1, count=10):
		""" google.com search engine

			framework  : core attribute
			q          : query for search
			key		   : API key
			ip		   : query on a given host IP
			limit      : count of pages
		"""
		self.framework = framework
		self.q = q
		self.key = key
		self._pages = ''
		self.limit = limit
		self.num = count
		self.shodan_api = f"https://api.shodan.io/shodan/host/search?key={self.key}&query={self.q}"
		self._links = []

	def run_crawl(self):
		self.framework.verbose('[SHODAN] Searching in shodan...')
		try:
			req = self.framework.request(self.shodan_api)
			print(req.text)
		except:
			self.framework.debug('[SHODAN] ConnectionError')
			self.framework.error('Shodan is missed!')
			return
		self._pages = req.text
		self._json_pages = req.json()

		# Key validation
		if 'errors' in self._json_pages:
			self.framework.error(f"[SHODAN] api key is incorrect:'self.key'")
			return

		# Request validation
		if not self._json_pages.get('data').get('accept_all'):
			self.framework.verbose('[SHODAN] request was not accepted!')
		else:
			self.acceptable = True

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		return self._links

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
