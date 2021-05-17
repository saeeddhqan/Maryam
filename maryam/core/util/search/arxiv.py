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
			""" arxiv.org search engine

					q         : query for search
					limit     : maximum result count
			"""
			self.framework = main.framework
			self.q = q
			self.max = limit
			self._rawxml = ''
			self._articles = []
			self._links = []
			self._links_with_data = []

		def run_crawl(self):
			self.q = urllib.parse.quote_plus(self.q)
			url = f'https://export.arxiv.org/api/query?search_query=all:'\
					   + f'{self.q}&start=0&max_results={self.max}'
			self.framework.verbose('[ARXIV] Searching the arxiv.org domain...')
			try:
					req = self.framework.request(url=url)
			except:
					self.framework.error('ConnectionError', 'arxiv', 'run_crawl')
					self.framework.error('ArXiv is missed!', 'arxiv', 'run_crawl')
					return
			self._rawxml = req.text
			self._articles = list(re.findall(r'<entry>(.*?)</entry>', 
					self._rawxml, 
					flags=re.DOTALL))

		@property
		def raw(self):
			return self._rawxml

		@property
		def articles(self):
			return self._articles

		@property
		def links(self):
			self._links = re.findall(r'(http://arxiv.org/abs/.*)<',
					self._rawxml)
			return self._links

		@property
		def links_with_data(self):
			findlink = lambda x: re.findall(r'(http://arxiv.org/abs/.*?)<', x)
			findauthors = lambda x: re.findall(r'<name>(.*?)</name>', x)
			findtitle = lambda x: re.findall(r'<title>(.*?)</title>', x, flags=re.DOTALL)

			for article in self._articles:
					self._links_with_data.append({'authors':findauthors(article),
							'title': list(map(html.unescape,findtitle(article))),
							'link' : findlink(article)
							})

			return self._links_with_data
