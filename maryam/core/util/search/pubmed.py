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
import urllib.parse
import html

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
			self._links_with_data = []
			self.pubmed = 'https://pubmed.ncbi.nlm.nih.gov'

		def run_crawl(self):
			self.q = urllib.parse.quote_plus(self.q)
			self.framework.verbose('Searching the pubmed domain...')

			url = f"https://pubmed.ncbi.nlm.nih.gov/?term={self.q}&size=200"
			try:
				req = self.framework.request(url=url)
			except Exception as e:
					self.framework.error(f"ConnectionError {e}.", 'util/pubmed', 'run_crawl')
					self.framework.error('Pubmed is missed!', 'util/pubmed', 'run_crawl')
					return
			self._rawhtml += req.text
			self._articles.extend(re.findall(r'<article .*?>(.*?)</article>', 
						req.text, 
						flags=re.DOTALL))

		@property
		def raw(self):
			return self._rawhtml

		@property
		def articles(self):
			return self._articles

		@property
		def links_with_data(self):
			findlink = lambda x: list(map(lambda x: self.pubmed+x, 
					re.findall(r'<a.*?class="docsum-title".*?href="(.*?)".*?>', x, flags=re.DOTALL)))
			findauthors = lambda x: re.findall(r'<span class="docsum-authors full-authors">(.*?)</span>', 
					x, flags=re.DOTALL)
			findtitle = lambda x: list(map(lambda x: html.unescape(re.sub('</?b>','',x)).strip(),
					re.findall(r'<a.*?class="docsum-title".*?>(.*?)</a>', x, flags=re.DOTALL)))

			for count,article in enumerate(self._articles):
					if count==self.max:
						break
					self._links_with_data.append({'authors':findauthors(article)[0],
							'title': findtitle(article)[0],
							'link' : findlink(article)[0]
							})

			return self._links_with_data
