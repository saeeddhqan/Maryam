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

from re import search

class main:

	def __init__(self, q, limit=2):
		""" baidu.com search engine
			
			q 		  : Query for search
			limit	  : Number of pages
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self.limit = 25 if limit > 25 else limit
		self._pages = ''
		self.baidu = 'baidu.com'

	def run_crawl(self):
		set_page = lambda x: x*10
		urls = [f"http://{self.baidu}/s?wd={self.q}&oq={self.q}&pn={set_page(i)}&ie=utf-8" for i in range(1, self.limit)]
		max_attempt = len(urls)
		for url in range(len(urls)):
			self.framework.verbose(f"[BAIDU] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url])
			except:
				self.framework.error('ConnectionError', 'util/baidu', 'run_crawl')
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Baidu is missed!', 'util/baidu', 'run_crawl')
					break
			else:
				self._pages += req.text

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
