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

from lxml import etree

class main:

	def __init__(self, q, limit=15):
		""" arxiv.org search engine

				q         : query for search
				limit     : maximum result count
		"""
		self.framework = main.framework
		self.q = q
		self.max = limit
		self._rawxml = ''
		self._tree = ''
		self._articles = []
		self._links = []
		self._results = []
		self.url = 'https://export.arxiv.org/api/query'
		self.NSMAP = {'w3':'http://www.w3.org/2005/Atom'}

	def run_crawl(self):
		payload = {'search_query': f"all:{self.q}", 'start': '0', 'max_results': self.max}
		self.framework.verbose('[ARXIV] Searching the arxiv.org domain...')
		try:
			req = self.framework.request(
					url=self.url,
					params=payload)
		except:
			self.framework.error('ConnectionError', 'arxiv', 'run_crawl')
			self.framework.error('ArXiv is missed!', 'arxiv', 'run_crawl')
			return
		self._rawxml = req.text
		self._tree = etree.fromstring(req.text.encode('utf-8'))
		self._articles = self.find(self._tree, './/w3:entry')


	def find(self, x, tofind):
		return x.findall(tofind, namespaces=self.NSMAP)

	@property
	def raw(self):
		return self._rawxml

	@property
	def articles(self):
		return self._articles

	@property
	def links(self):
		self._links = list(map(lambda x: x.text, 
			self.find(self._tree, './/w3:id')))
		return self._links

	@property
	def results(self):
		findlink = lambda x: self.find(x, './/w3:id')[0].text
		findauthors = lambda x: ', '.join(list(map(lambda x: x.text, 
				self.find(x, './/w3:author/w3:name'))))
		findtitle = lambda x: self.find(x, './/w3:title')[0].text
		findsummary = lambda x: self.find(x, './/w3:summary')[0].text.strip()

		for article in self._articles:
			self._results.append({
				't': findtitle(article),
				'a': findlink(article),
				'c': findauthors(article),
				'd': findsummary(article)
				})

		return self._results
