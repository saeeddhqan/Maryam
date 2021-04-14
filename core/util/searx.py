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

class main:

	def __init__(self, q, limit=1):
		""" searx search engine

			q	: Query for search
			limit	: Number of Pages

		"""
		self.framework = main.framework
		self.q = q
		self.agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
		self._pages = ''
		self.limit = limit
		self._links = []
		self._json = {}
		self.searx = ['https://searx.prvcy.eu/search', 'https://searx.xyz/search', 'https://searx.bar/search']

	def run_crawl(self):
		self._json['results'] = [] 
		for url in self.searcx:
			params = {'category_general': 1, 'q': self.q, 
				  'pageno': 1, 'time_range': None, 
				  'language': 'en-US', 'format': 'json'}
			max_attempts = 0
			while True:
				self.framework.verbose(f"[SEARX] Searching {url} page {params['pageno']}...", end='\r')
				try:
					req = self.framework.request(
						url=url,
						params=params,
						headers={'User-Agent': self.agent},
						allow_redirects= True)
				except Exception as e:
					self.framework.error(f"ConnectionError: {e}", 'util/searx', 'run_crawl')
					max_attempts += 1
					if max_attempts == self.limit:
						self.framework.error(f"Searx {url} is missed!", 'util/searx', 'run_crawl')
						return
				else:
					self._pages += req.text
					try:
						self._json['results'] += req.json()['results']
					except:
						self.framework.error(f"Searx {url} is missed!", 'util/searcx', 'run_crawl')
					params['pageno'] += 1
					if params['pageno'] >= self.limit:
						break

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		for result in self._json['results']:
			self._links.append(result['url'])
		return self._links

	@property
	def results(self):
		results = []
		for result in self._json['results']:
			if 'content' in resunt:
				content = result['content']
			else:
				content = 'No description provided'
			cite = self.framework.meta_search_util().make_cite(result['url'])
			self._links_with_data.append({
				'title': result['title'],
				'a': result['url'],
				'cite': cite,
				'content': content
			})

		return results
	
	@property
	def json(self):
		return self._json

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)
	
	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q)
