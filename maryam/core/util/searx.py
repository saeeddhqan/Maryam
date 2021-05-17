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
		self._pages = ''
		self.limit = limit
		self._links = []
		self._json = {}
		self.searx = ['https://searx.prvcy.eu/search', 'https://searx.xyz/search', 'https://searx.nevrlands.de/searx/search', 'https://searx.info/search']

	def run_crawl(self):
		page = 1
		self._json['results'] = [] 
		params = {'category_general': 1, 'q': self.q, 
			  'pageno': 1, 'time_range': None, 
			  'format': 'json'}
		max_attempts = 0
		for url in self.searx:
			while True:
				self.framework.verbose(f"[SEARX] Searching {url} page {params['pageno']}...", end='\r')
				try:
					req = self.framework.request(
						url=url,
						params=params,
						allow_redirects= True)
				except Exception as e:
					self.framework.error(f"ConnectionError: {e}", 'util/searx', 'run_crawl')
					max_attempts += 1
					if max_attempts == self.limit:
						self.framework.error(f"Searx {url} is missed!", 'util/searx', 'run_crawl')
						return
				else:
					self._pages += req.text
					if req.status_code == 200 and 'results' in req.json():
						self._json['results'] += req.json()['results']
					else:
						self.framework.error(f"Searx {url} is missed!", 'util/searcx', 'run_crawl')
						break
					if params['pageno'] >= self.limit:
						return
					params['pageno'] += 1

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
			if 'content' in result:
				content = result['content']
			else:
				content = 'No description provided'
			cite = self.framework.meta_search_util().make_cite(result['url'])
			results.append({
				't': result['title'],
				'a': result['url'],
				'c': cite,
				'd': content
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
