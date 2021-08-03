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

	def __init__(self, q, limit=1):
		""" metacrawler.com search engine

			q 		  : query for search
			limit	  : count of pages
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self.limit = limit
		self._pages = ''
		self.metacrawler = 'metacrawler.com'

	def run_crawl(self):
		urls = [f"http://{self.metacrawler}/serp?q={self.q}&page={i}" for i in range(1, self.limit+1)]
		max_attempt = len(urls)

		for url in range(len(urls)):
			self.framework.verbose(f"[METACRAWLER] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url])
			except:
				self.framework.error('ConnectionError', 'util/metacrawler', 'run_crawl')
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Metacrawler is missed!')
					break
			else:
				page = self.framework.to_str(req.text)
				if 'To continue, please respond below:' in page:
					self.framework.error('CaptchaError', 'util/metacrawler', 'run_crawl')
					return
				if url > 0:
					if 'Next »' not in page:
						self._pages += page
						break
				self._pages += page

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		links = self.framework.page_parse(self._pages).findall(\
			r'<a class="web-bing__title" href="(.*)"\sdata-thash')
		return links

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)
	
	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)
	
	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
