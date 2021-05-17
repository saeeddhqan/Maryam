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

class main:

	def __init__(self, q, limit=2):
		""" qwant.com search engine

			q 		  : Query for search
			limit	  : Number of pages
		"""
		self.framework = main.framework
		self.q = q
		self.limit = limit
		self._pages = ''
		self._json = []
		self._links = []
		self._links_with_title = []
		self.qwant = 'qwant.com'

	def run_crawl(self, method='webpages'):
		policies = {'webpages': 'web',
					'images': 'images',
					'news': 'news',
					'videos': 'videos'}

		method = method.lower()
		if method not in policies:
			search_type = policies.get('webpages')
		else:
			search_type = policies[method]
		set_page = lambda x: x*10
		urls = [f'https://api.{self.qwant}/api/search/{search_type}?q={self.q}&t=web&device=desktop&safesearch=1&uiv=4&count=10&offset={set_page(i)}' 
					for i in range(self.limit)]
		headers = {'Host': 'api.qwant.com', 
				   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
				   'Accept-Language': 'en-US,en;q=0.5en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 
				   'Connection': 'keep-alive', 'Cookie': 'JSESSIONID=6120E7C52197190DE5126DCBF47D38B0', 
				   'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0'}
		for url in range(len(urls)):
			self.framework.verbose(f"[QWANT] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url], headers=headers)
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/qwant', 'name_crawl')
				self.framework.error('Qwant is missed!', 'util/qwant', 'name_crawl')
			else:
				if req.status_code == 429 and "I can't let you do that..." in req.text and '<div class="error-code">' in req.text:
					self.framework.error('429 Too Many Requests')
					return
				self._pages += req.text
				try:
					self._json.append(req.json())
				except Exception as e:
					self.framework.error('429 Too Many Requests')
					return
				else:
					if req.json() == {"status": "error", "error": 22}:
						self.framework.error('429 Too Many Requests')

	@property
	def pages(self):
		return self._pages

	@property
	def json(self):
		return self._json

	@property
	def links(self):
		for page in self.json:
			results = page.get('data', {}).get('result', {}).get('items', {})
			self._links.extend([x.get('url') for x in results])
		return self._links

	@property
	def links_with_title(self):
		for page in self.json:
			items = page.get('data', {}).get('result', {}).get('items', {})
			if not items:
				return []
			for item in items:
				self._links_with_title.append([item['title'].replace('<b>','').replace('</b>', ''), item['url']])
		return self._links_with_title

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q, self.links)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
