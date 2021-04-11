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
from bs4 import BeautifulSoup as bs

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
			self._links_with_data = []

		def run_crawl(self):
			self.q = self.framework.urlib(self.q).quote
			self.framework.verbose('Searching Gigablast...')
			try:
				first_url = f'https://www.gigablast.com/search?q={self.q}&format=json'
				req = self.framework.request(url=first_url)

				soup = bs(req.text,'html.parser')
				script = soup.find('body')['onload']
				rand = re.findall(r'rand=(\d+[^&]+)&x', script)[0]
				xkhh = re.findall(r"khh=(\d+[^']+)'", script)[0]
				final_url =  ''.join([f'https://www.gigablast.com/search?',
					f'q={self.q}&format=json&rand={rand}&xkhh={xkhh}'])

				req = self.framework.request(url=final_url)
				self._json = req.json()['results']
			except:
				self.framework.error('ConnectionError.', 'util/gigablast', 'run_crawl')
				self.framework.error('Gigablast is missed!', 'util/gigablast', 'run_crawl')

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
		def links_with_data(self):
			for count, result in enumerate(self._json):
				if count>=self._max:
					break
				self._links_with_data.append({
					'title': result['title'],
					'subtitle': result.get('subTitle'),
					'summary': result['sum'],
					'link': result['url']
					})
			return self._links_with_data
