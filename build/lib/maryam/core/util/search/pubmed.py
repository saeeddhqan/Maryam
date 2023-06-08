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

import lxml

class main:

	def __init__(self, q, count=15):
		""" pubmed.ncbi.nlm.nih.gov search engine

				q         : query for search
				count     : maximum result count
		"""
		self.framework = main.framework
		self.q = q
		self.max = count
		self._rawhtml = ''
		self._results = []
		self.pubmed = 'https://pubmed.ncbi.nlm.nih.gov'
		self.xpath_names = {
			'results': './/article',
			'results_content':'.//div[@class="full-view-snippet"]',
			'results_title':'.//a[@class="docsum-title"]',
			'results_a': './/a[@class="docsum-title"]',
			'results_cite': './/span[@class="docsum-authors full-authors"]'
		}
		self.xpaths = {
			self.xpath_names['results']: [
				self.xpath_names['results_content'],
				self.xpath_names['results_title'],
				self.xpath_names['results_a'],
				self.xpath_names['results_cite']
			]
		}

	def run_crawl(self):
		self.framework.verbose('Searching the pubmed domain...')

		payload = {'term': self.q, 'size': 200}
		try:
			req = self.framework.request(
					url=self.pubmed,
					params=payload)
		except Exception as e:
			self.framework.error(f"ConnectionError {e}.", 'util/pubmed', 'run_crawl')
			self.framework.error('Pubmed is missed!', 'util/pubmed', 'run_crawl')
			return

		self._rawhtml += req.text

	@property
	def raw(self):
		return self._rawhtml

	@property
	def results(self):
		parser = self.framework.page_parse(self._rawhtml)
		results = parser.get_engine_results(self.xpaths, self.xpath_names)

		for count,article in enumerate(results):
			if count == self.max:
				break
			self._results.append({
				't': article['t'],
				'a': self.pubmed + article['a'],
				'c': article['c'],
				'd': article['d'] if len(article['d']) > 0 else 'No abstract available'
				})

		return self._results
