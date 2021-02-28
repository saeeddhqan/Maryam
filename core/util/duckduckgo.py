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

	def __init__(self, framework, q, limit=1, count=10):
		""" google.com search engine

			framework  : core attribute
			q          : query for search
			limit      : count of pages
			google_api : google api(if you need to use api_run_crawl)
			google_cx  : google cx(if you need to use api_run_crawl)
		"""
		self.framework = framework
		self.q = q
		self.agent = framework.rand_uagent().lynx[7]
		self._pages = ''
		self.limit = limit+1
		self._links = []

	def run_crawl(self):
		#url = f"https://api.duckduckgo.com/?q={self.q}&ia=web"
		url =f"https://html.duckduckgo.com/html?q={self.q}&t=h_&ia=web"
		#url = f"https://www.google.com/search?q={self.q}"
		print(self.q)
		self.framework.verbose(f'[DUCKDUCKGO] Processing your request...', end='\r')
		try:
			req = self.framework.request(
					url=url,
					headers={"User-Agent":self.agent})
		except:
			self.framework.error('[DUCKDUCKGO] ConnectionError')
			return
		print(req.text)
		links = self.framework.page_parse(req.text).findall(r'href="([^"]+)"')
		#print(links)

		for link in set(links):
			self._links.append(self.framework.urlib(link).unquote_plus)



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
