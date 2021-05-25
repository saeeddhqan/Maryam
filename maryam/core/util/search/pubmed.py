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

	def __init__(self, q, limit=15):
		""" pubmed.ncbi.nlm.nih.gov search engine

				q         : query for search
				limit     : maximum result count
		"""
		self.framework = main.framework
		self.q = q
		self.max = limit
		self._rawhtml = ''
		self._articles = []
		self._links = []
		self._results = []
		self.pubmed = 'https://pubmed.ncbi.nlm.nih.gov'

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
		doc = lxml.html.document_fromstring(req.text)
		self._articles = doc.findall('.//article')

	@property
	def raw(self):
		return self._rawhtml

	@property
	def articles(self):
		return self._articles

	@property
	def results(self):
		findlink = lambda x: self.pubmed + x.find_class('docsum-title')[0].attrib['href']
		findauthors = lambda x: x.find('.//span[@class="docsum-authors full-authors"]').text_content()
		findtitle = lambda x: x.find_class('docsum-title')[0].text_content().strip()
		findsummary = lambda x: x.find_class('full-view-snippet')[0].text_content().strip()

		for count,article in enumerate(self._articles):
			if count==self.max:
				break
			d = findsummary(article)
			self._results.append({
				't': findtitle(article),
				'a': findlink(article),
				'c': findauthors(article),
				'd': d if len(d)>0 else 'No abstract available'
				})

		return self._results
