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
				limit     : maximum result count
		"""
		self.framework = main.framework
		self.q = q
		self.limit = limit
		self._json = []
		self._results = []
		self.url = 'https://core.ac.uk/search/api/search'

	def run_crawl(self):
		self.framework.verbose('Searching the CORE domain...')

		data = f'{{"basicQuery":{{"count":"{self.limit}","searchCriteria":"{self.q}","offset":0}}}}'
		try:
			req = self.framework.request(
					url=self.url,
					method='POST',
					data=data,
					)
		except Exception as e:
			self.framework.error(f"ConnectionError {e}.", 'util/search/core_ac', 'run_crawl')
			self.framework.error('CORE.AC.UK is missed!', 'util/search/core_ac', 'run_crawl')
			return
		else:
			self._json = req.json()

	@property
	def json(self):
		return self._json

	@property
	def results(self):
		findlink = lambda x: x["downloadUrl"]
		findauthors = lambda x: x.get("authorsString")
		findtitle = lambda x: x["title"]
		findsummary = lambda x: x.get("snippet")

		for count,article in enumerate(self._json['results']):
			if count == self.limit:
				break
			d = findsummary(article)
			c = findauthors(article)
			self._results.append({
				't': findtitle(article),
				'a': findlink(article),
				'c': c if c is not None else 'Authors not available',
				'd': re.sub('<[^<]+?>', '', d) if d is not None\
						else 'Abstract not available'
				})

		return self._results
