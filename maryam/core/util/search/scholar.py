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
		""" scholar.google.com search engine

			q	  : query for search
			limit	  : maximum result count
		"""
		self.framework = main.framework
		self.q = q
		self.max = limit
		self._articles = []
		self._results = []

	def run_crawl(self):
		start = 0
		self.framework.verbose('Searching the scholar.google.com domain...')
		for start in range(0, (self.max//10)+1):
			url = f"https://scholar.google.com/scholar"
			payload = {'as_vis': '1', 'q': self.q, 'start': start}
			try:
				req = self.framework.request(
						url=url,
						params=payload)
			except:
				self.framework.error('[SCHOLAR] ConnectionError', 'util/search/scholar', 'run_crawl')
				self.framework.error('Google Scholar is missed!', 'util/search/scholar', 'run_crawl')
			else:
				doc = lxml.html.document_fromstring(req.text)
				self._articles.extend(doc.find_class('gs_ri'))
				start += 10
	
	@property
	def articles(self):
		return self._articles

	@property
	def results(self):
		findlink = lambda x: x.xpath('h3/a')[0].attrib['href']
		findauthors = lambda x: x.find_class('gs_a')[0].text_content()
		findtitle = lambda x: x.xpath('h3/a')[0].text_content()
		finddesc = lambda x: x.find_class('gs_rs')[0].text_content()

		for count,article in enumerate(self._articles):
			if count==self.max:
				break
			self._results.append({
				't': findtitle(article),
				'a': findlink(article),
				'c': findauthors(article),
				'd': finddesc(article)
				})

		return self._results
