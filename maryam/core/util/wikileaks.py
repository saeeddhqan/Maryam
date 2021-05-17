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
from bs4 import BeautifulSoup as bs

class main:

	def __init__(self, q, limit=1):
		""" wikileaks.org search engine

			q		: Query for search
			limit	: Number of Pages

		"""

		self.framework = main.framework
		self.q = q
		self.agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
		self._pages = ''
		self.limit = limit
		self._links = []
		self._results = []
		self._links_with_data = []

	def run_crawl(self):
		max_attempts = 0
		url = 'https://search.wikileaks.org/advanced'
		params = {'query': self.q, 'include_external_sources': True, 'page': 1}
		while True:
			self.framework.verbose(f"[WIKILEAKS] Searching in {params['page']} page ....", end='\r')
			try:
				req = self.framework.request(
					url=url,
					params=params,
					headers={'User-Agent': self.agent},
					allow_redirects=True)
			except Exception as e:
				self.framework.error(f"ConnectionError: {e}", 'util/wikileaks', 'run_crawl')
				max_attempts += 1
				if max_attempts == self.limit:
					self.framework.error('Wikileaks is missed!', 'util/wikileaks', 'run_crawl')
					return
			else:
				self._pages += req.text
				params['page'] += 1
				if params['page'] >= self.limit:
					break

		soup = bs(self._pages, 'html.parser')
		self._results = soup.find_all('div', class_='info')
		for result in self._results:
			self._links.append(result.find_all('a')[0]['href'])

	@property
	def pages(self):
		return self._pages
	
	@property
	def links(self):
		return self._links

	@property
	def links_with_data(self):
		for result in self._results:
			self._links_with_data.append({
				'title': result.find_all('a')[0].text,
				'link': result.find_all('a')[0]['href']
				})
		
		return self._links_with_data

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
