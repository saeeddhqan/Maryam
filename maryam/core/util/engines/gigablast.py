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
import json

class main:

		def __init__(self, q, limit=15):
			""" Gigablast search engine
					q     : Query to search
					limit : Number of pages
			"""
			self.framework = main.framework
			self.q = q
			self._max = limit
			self._json = ''
			self._results = []

		def run_crawl(self):
			from bs4 import BeautifulSoup as bs

			self.q = self.framework.urlib(self.q).quote
			self.framework.verbose('Searching Gigablast...')
			first_url = 'https://www.gigablast.com/search'
			payload = {'q': self.q, 'format': 'json'}
			try:
				req = self.framework.request(url=first_url,
						params=payload)
			except:
				self.framework.error('ConnectionError.', 'util/gigablast', 'run_crawl')
				self.framework.error('Gigablast is missed!', 'util/gigablast', 'run_crawl')
			else:
				soup = bs(req.text,'html.parser')
				script = soup.find('body')['onload']
				params1 = re.findall(r"var uxrl='/search(.*?)'", script)[0]
				params2 = re.findall(r"uxrl=uxrl\+'(.*?)'", script)[0]
				final_url = first_url + params1 + params2
				try:
					req = self.framework.request(url=final_url)
				except:
					self.framework.error('ConnectionError.', 'util/gigablast', 'run_crawl')
					self.framework.error('Gigablast is missed!', 'util/gigablast', 'run_crawl')
				else:
					self._json = req.json()['results']

		@property
		def json(self):
			return self._json

		@property
		def raw(self):
			return json.dumps(self._json)

		@property
		def dns(self):
			return self.framework.page_parse(self.raw).get_dns(self.q)

		@property
		def emails(self):
			return self.framework.page_parse(self.raw).get_emails(self.q)

		@property
		def docs(self):
			return self.framework.page_parse(self.raw).get_docs(self.q)

		@property
		def results(self):
			for count, result in enumerate(self._json):
				if count >= self._max:
					break
				urlib = self.framework.urlib(result['url'])
				a = urlib.unquote
				cite = result.get('subTitle') or self.framework.meta_search_util().make_cite(a)
				self._results.append({
					't': result['title'],
					'a': a,
					'c': cite,
					'd': result['sum'],
					})
			return self._results
