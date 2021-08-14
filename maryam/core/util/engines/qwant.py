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
		self.qwant = 'https://api.qwant.com/v3/search/web'

	def run_crawl(self):
		page = 1
		set_page = lambda x: (x - 1) * 10 + 1
		payload = {'q': self.q, 'offset': set_page(page), 'count': '10', 'safesearch': '0', 'device': 'desktop', 'locale': 'en_us'}
		headers = {'Host': 'api.qwant.com', 
				   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
				   'Accept-Language': 'en-US,en;q=0.5en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 
				   'Connection': 'keep-alive', 'Cookie': 'JSESSIONID=6120E7C52197190DE5126DCBF47D38B0', 
				   'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0'}
		while True:
			self.framework.verbose(f"[QWANT] Searching in {page+1} page...")
			try:
				# req = self.framework.request(url=self.qwant, headers=headers, params=payload)
				req = self.framework.request(url=self.qwant, params=payload)
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/engines/qwant', 'name_crawl')
				self.framework.error('Qwant is missed!', 'util/engines/qwant', 'name_crawl')
				break
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
					if req.json() == {'status': 'error', 'data': {'error_code': 22}}:
						self.framework.error('429 Too Many Requests')
						return
					else:
						if page == self.limit:
							break
						page += 1
						payload['offset'] = set_page(page)

	@property
	def pages(self):
		return self._pages

	@property
	def json(self):
		return self._json

	@property
	def links(self):
		for page in self._json:
			results = page.get('data', {}).get('result', {}).get('items', {})
			self._links.extend([x.get('url') for x in results])
		return self._links

	@property
	def results(self):
		results = []
		for page in self._json:
			items = page.get('data', {}).get('result', {})
			if items:
				items = items.get('items', {})
				if items:
					items = items.get('mainline', {})
			for item in items:
				inside_items = item.get('items')
				for i in inside_items:
					a = i['url']
					result = {
						't': i['title'],
						'a': a,
						'c': self.framework.meta_search_util().make_cite(a),
						'd': '' if 'desc' not in i else i.get('desc'),
					}
					results.append(result)
		return results

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q, self.links)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
