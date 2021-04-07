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

import json

class main:
	def __init__(self, q, limit):

		self.framework = main.framework
		self.q = q
		self.limit = limit
		self._pages = ''
		self._json = {}
		self._links = []
		self._json_links = []

	def run_crawl(self):
		url = 'https://cse.google.com/cse/element/v1'
		params = {'rsz': 'filtered_cse', 'num': self.limit, 'hl': 'en', 
				  'source': 'gcsc', 'start': 0, 'gss': '.co', 'cselibv': '323d4b81541ddb5b',
				  'cx': 'partner-pub-3426987762009703:6481020877', 'q': self.q,
				  'safe': 'active', 'cse_tok': 'AJvRUv2j70Wv82apD6mZynCCFiFb:1617800006292',
				  'exp': 'csqr,cc', 'callback': 'google.search.cse.api4433'}
		
		self.framework.verbose('Searching in searchportal.co ...')
		try:
			req = self.framework.request(
				url=url,
				params=params,
				)
		except Exception as e:
			self.framework.error(f"[searchportal] ConnectionError: {e}")
			self.framework.error('searchportal in missed!')
		else:
			self._pages = req.text
			try:
				self._json = json.loads(req.text[34:-2])
			except:
				if req.status_code in (400,):
					self.framework.error('The server cannot process the request because it is malformed')
				self.framework.error('searchportal is missed!')

	@property
	def pages(self):
		return self._pages
	
	@property
	def links(self):
		resp = self._json.get('results')
		if resp:
			for result in resp:
				self._links.append(result.get('url'))
		return self._links

	@property
	def json(self):
		return self._json

	@property
	def json_links(self):
		resp = self._json.get('results')
		if resp:
			for result in resp:
				self._json_links.append(result)
		return self._json_links
	

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self.pages).get_docs(self.q)
