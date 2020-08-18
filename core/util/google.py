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
import os

class main:

	def __init__(self, framework, q, limit=1, count=10, google_api=None, google_cx=None):
		""" google.com search engine

			framework  : core attribute
			q          : query for search
			limit      : count of pages
			google_api : google api(if you need to use api_run_crawl)
			google_cx  : google cx(if you need to use api_run_crawl)
		"""
		self.framework = framework
		self.q = q
		self.agent = framework.rand_uagent().lynx[0]
		self._pages = ''
		self.limit = limit
		self.num = count
		self.google_api = google_api
		self.google_cx = google_cx
		self._links = []

	def run_crawl(self):
		page = 1
		url = 'https://google.com/search'
		set_page = lambda x: (x - 1) * self.num
		payload = {'num' : self.num, 'start' : set_page(page), 'ie' : 'utf-8', 'oe' : 'utf-8', 'q' : self.q, 'filter': '0'}
		max_attempt = 0
		while True:
			self.framework.verbose(f'[GOOGLE] Searching in {page} page...', end='\r')
			try:
				req = self.framework.request(
					url=url,
					params=payload,
					allow_redirects=False)
			except:
				self.framework.error('[GOOGLE] ConnectionError')
				return

			if req.status_code == 503:
				req = self.framework.error('[GOOGLE] Google CAPTCHA triggered.')
				break

			if req.status_code in [301, 302]:
				redirect = req.headers['location']
				req = self.framework.request(url=redirect, allow_redirects=False)

			self._pages += req.text
			page += 1
			payload['start'] = set_page(page)
			if page >= self.limit:
				break
		links = self.framework.page_parse(self._pages).findall(r'a href="([^"]+)" onmousedown')
		for link in links:
			cond1 = 'https://support.google.com/' not in link.lower()
			if cond1:
				self._links.append(self.framework.urlib(link).unquote_plus)

	def api_run_crawl(self):
		if not (self.google_api and self.google_cx):
			self.framework.error('[GOOGLEAPI] google api needs google_api and google_cx variable')
			return

		url = 'https://www.googleapis.com/customsearch/v1'
		payload = {'alt': 'json', 'prettyPrint': 'false', 'key': self.google_api, 'cx': self.google_cx, 'q': query}
		page = 0
		self.verbose(f"[GOOGLEAPI] Searching Google API for: {self.q}")
		while True:
			self.framework.verbose(f'[GOOGLE] Searching in {page} page...', end='\r')
			resp = self.framework.request(url, params=payload)
			if resp.json() == None:
				raise self.framework.FrameworkException(f"Invalid JSON response.{os.linesep}{resp.text}")
			# add new results
			if 'items' in resp.json():
				self._links.extend(resp.json()['items'])
			# increment and check the limit
			page += 1
			if limit == page:
				break
			# check for more pages
			if not 'nextPage' in resp.json()['queries']:
				break
			payload['start'] = resp.json()['queries']['nextPage'][0]['startIndex']

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		return self._links

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
