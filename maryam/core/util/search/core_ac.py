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

	def __init__(self, q, limit=10):
		""" core.ac.uk search engine

				q         : query for search
				limit     : maximum page search
		"""
		self.framework = main.framework
		self.q = q
		self.limit = limit
		self._pages = ''
		self._jsons = []
		self._results = []
		self.url = 'https://core.ac.uk/search/_next/data/-JCaNMETLG_pZxb60WhOp/search.json'

	def run_crawl(self):
		self.framework.verbose('Searching the CORE domain...')
		page = 1
		payload = {'q': self.q, 'page': 1}
		max_attempt = 0
		while True:
			try:
				req = self.framework.request(
						url=self.url,
						method='GET',
						params=payload,
						)
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/search/core_ac', 'run_crawl')
				max_attempt += 1
				if max_attempt == self.limit:
					self.framework.error('CORE.AC.UK is missed!', 'util/search/core_ac', 'run_crawl')
					break
			else:
				self._pages += req.text
				self._jsons.append(req.json())
				page += 1
				payload['page'] = page
				if page >= self.limit:
					break

	@property
	def json(self):
		return self._json

	@property
	def results(self):
		findlink = lambda x: x['downloadUrl']
		findauthors = lambda x: [i.get('name', '') for i in x.get('authors', [])]
		findtitle = lambda x: x['title']
		findsummary = lambda x: x.get('abstract')
		for page in self._jsons:
			for article in enumerate(page['pageProps']['data']['results']):
				article = article[1]
				d = findsummary(article)[:100] + '...'
				c = findauthors(article)
				c = ','.join(c)[:100] or '' + '...'
				self._results.append({
					't': findtitle(article),
					'a': findlink(article),
					'c': c,
					'd': d,
				})

		return self._results
