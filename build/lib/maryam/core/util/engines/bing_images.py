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

from lxml import html
from json import loads

class main:
	def __init__(self, q, limit=3, count=28):
		""" bing.com search engine
			q     : Query for search
			limit : Number of pages
			count : Number of results
		"""
		self.framework = main.framework
		self.q = q
		self.agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'
		self.url = 'https://www.bing.com/images/search'
		self._pages = ''
		self.count = 28 if count > 28 else count
		self.limit = 10 if limit > 10 else limit

	def run_crawl(self):
		set_page = lambda x: (x*self.count)+1
		payload = {'count': self.count, 'first': 1, 'form': 'IBASEP', 'q': self.q}
		max_attempt = 0
		for i in range(self.limit):
			self.framework.verbose(f"[BING Image] Searching in {i} page...", end='\r')
			try:
				req = self.framework.request(
					url=self.url,
					params=payload,
					headers={'user-agent': self.agent},
					allow_redirects=True)
			except Exception as e:
				self.framework.error(f"ConnectionError: {e}", 'util/engines/bing_images', 'run_crawl')
				max_attempt += 1
				if max_attempt == self.limit:
					self.framework.error('Bing is missed!', 'util/engines/bing_images', 'run_crawl')
					break
			else:
				self._pages += req.text
				payload['first'] = set_page(i+1)

	@property
	def results(self):
		items = []
		tree = html.fromstring(self._pages)
		for item in tree.xpath('//div[@class="imgpt"]'):
			try:
				info = item.xpath('.//div[@class="img_info hon"]')[0].xpath("./span[@class='nowrap']")[0].text
				m = loads(item.xpath('./a/@m')[0])
				title = m.get('t', '').replace(u'\ue000', '').replace(u'\ue001', '')
				items.append({'i': m['murl'],
								't': title,
								'a': m['purl'],
								'd': info
								})
			except:
				continue
		return items

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		return [x['a'] for x in self.results]

