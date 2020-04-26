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

	def __init__(self, framework, q, count=30):
		""" searchencrypt.com search engine

			framework : core attribute
			q 		  : query for search
			count	  : count of links
		"""
		self.framework = framework
		self.q = q
		self.count = count
		self._pages = ''
		self._json = {}
		self._links = []
		self._links_with_title = {}
		self.searchencrypt = 'searchencrypt.com'

	def run_crawl(self, policy='webpages'):
		policies = {'webpages': 'web',
					'images': 'web,image',
					'news': 'news'}

		policy = policy.lower()
		if policy not in policies:
			search_type = policies['webpages']
		else:
			search_type = policies[policy]

		url = f"https://spapi.{self.searchencrypt}/api/search?q={self.q}&types={search_type}&limit={self.count}"
		self.framework.verbose('Opening the searchencrypt.com domain...', end='\r')
		try:
			req = self.framework.request(url=url)
		except:
			self.framework.error('[SEARCHENCRYPT] ConnectionError')
			self.framework.error('Searchencrypt is missed!')
			return

		pages = req.text
		self._json = req.json()

	@property
	def pages(self):
		return self._pages

	@property
	def json(self):
		return self._json

	@property
	def links(self):
		results = self.json.get('Results')
		self._links = [x.get('ClickUrl') for x in results]
		return self._links

	@property
	def links_with_title(self):
		results = self.json.get('Results')
		if not results:
			return {}
		self._links_with_title = {x.get('Title'): x.get('ClickUrl') for x in results}
		return self._links_with_title

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q, self.links)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
