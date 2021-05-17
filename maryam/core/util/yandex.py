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
import webbrowser

class main:

	def __init__(self, q, limit=2, count=100):
		""" yandex.com search engine

			q 		  : query for search
			limit	  : Number of pages
			count	  : Number of links
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self.count = count
		self.limit = limit
		self._pages = ''
		self.yandex = 'yandex.com'

	def run_crawl(self):
		urls = [f"https://{self.yandex}/search?text={self.q}&numdoc={self.count}&p={i}" for i in range(1, self.limit+1)]
		max_attempt = len(urls)
		for url in range(len(urls)):
			self.framework.debug(f"[YANDEX] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url], allow_redirects=True)
			except:
				self.framework.error('ConnectionError', 'util/yandex', 'run_crawl')
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Yandex is missed!', 'util/yandex', 'run_crawl')
					break
			else:
				if '<title>Oops!</title>' in req.text:
					self.framework.error('Yandex CAPTCHA triggered.', 'util/yandex', 'run_crawl')
					return

				page = req.text
				if ']">next</a>' not in page:
					self._pages += page
					break
				self._pages += page

	@property
	def pages(self):
		return self._pages

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q)
