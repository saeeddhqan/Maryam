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

	def __init__(self, q, limit):
		""" exalead.com search engine

			q         : Query for search
			limit     : Number of pages
		"""
		self.framework = main.framework
		self.q = q
		self._pages = ''
		self.exalead = 'www.exalead.com'
		self.limit = limit

	def run_crawl(self):
		set_page = lambda x:x*10
		urls = [f"https://{self.exalead}/search/web/results/?q={self.q.replace(' ', '%20')}&elements_per_page=50&start_index={set_page(i)}" 
					for i in range(self.limit+1)]
		max_attempt = len(urls)
		for url in range(max_attempt):
			self.framework.debug(f"[EXALEAD] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url])
			except:
				self.framework.error('ConnectionError.', 'util/exalead', 'run_crawl')
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Exalead is missed!', 'util/exalead', 'run_crawl')
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
