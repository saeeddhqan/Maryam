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
		self.millionshort = 'millionshort.com'

	def run_crawl(self):
		payloads = {'keywords': self.q, 'remove': '0', 'offset': '0'}
		baseurl = f"https://{self.millionshort}/api/search"
		set_page = lambda x: x*10
		urls = [f'https://{self.millionshort}/api/search?keywords={self.q}&remove=0&offset={set_page(i)}'
					for i in range(self.limit)]
		for url in range(len(urls)):
			self.framework.verbose(f"[MILLIONSHORT] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url])
			except:
				self.framework.error('ConnectionError')
			else:
				if 'captcha' in req.json():
					self.framework.error('CaptchaError', 'util/millionshort', 'run_crawl')
					return
				self._pages += req.text
				self._json.append(req.json())

	@property
	def pages(self):
		return self._pages

	@property
	def json(self):
		return self._json

	@property
	def links(self):
		for page in self.json:
			results = page.get('content', {}).get('webPages', {})
			self._links.extend([x.get('displayUrl') for x in results])
		return self._links

	@property
	def links_with_title(self):
		json = self.json
		if not json:
			return {}
		for page in self.json:
			results = page.get('content', {}).get('webPages', {})
			self._links_with_title.update({x.get('name'): x.get('displayUrl') for x in results})
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
