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
		""" millionshort.com search engine

			q 		  : query for search
			limit	  : Number of pages
		"""
		self.framework = main.framework
		self.q = q
		self.limit = limit
		self._pages = ''
		self._json = []
		self._links = []
		self._links_with_title = {}
		self.millionshort = 'https://millionshort.com/api/search'

	def run_crawl(self):
		page = 1
		set_page = lambda x: (x - 1) * 10 + 1
		payload = {'keywords': self.q, 'remove': '0', 'offset': '0'}
		headers = {
			"Host": 'millionshort.com',
			"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
			"Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			"Accept-Language": 'en-US,en;q=0.5',
			"Accept-Encoding": 'gzip, deflate, br',
			"Connection": 'keep-alive',
			"Cookie": 'connect.sid=s%3AVZd6oWjMPfegJTrCK6iVYs8p1S4q3Q-h.OC7iYFkDE5A2u6%2BsJkCa96q6ituwLnNDh0EjzEJhvNk',
			"Upgrade-Insecure-Requests": '1',
			"If-None-Match": 'W/"9fc-Kb1JjxDz/K4kA1S7nkbpkibKV94"',
			"Cache-Control": 'max-age=0'
		}
		while True:
			self.framework.verbose(f"[MILLIONSHORT] Searching in {page} page...")
			try:
				req = self.framework.request(url=self.millionshort, params=payload, headers=headers)
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/engines/millionshort', 'name_crawl')
				self.framework.error('millionshort is missed!', 'util/engines/millionshort', 'name_crawl')
				break
			else:
				if 'captcha' in req.json():
					self.framework.error('CaptchaError', 'util/engines/millionshort', 'run_crawl')
					self.framework.error('millionshort is missed!', 'util/engines/millionshort', 'name_crawl')
					return
				self._json.append(req.json())
				self._pages += req.text
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
			results = page.get('content', {}).get('webPages', {})
			self._links.extend([x.get('displayUrl') for x in results])
		return self._links

	@property
	def results(self):
		results = []
		for page in self._json:
			items = page.get('content', {}).get('webPages', {})
			for item in items:
				a = item['displayUrl']
				result = {
					't': item['name'],
					'a': a,
					'c': self.framework.meta_search_util().make_cite(a),
					'd': item['snippet'],
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
