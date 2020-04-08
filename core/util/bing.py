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

	def __init__(self, framework, q, limit=1, count=10):
		""" bing.com search engine
			
			framework : core attribute
			q 		  : query for search
			limit	  : count of pages
			count	  : count of links
		"""
		self.framework = framework
		self.q = self.framework.urlib(q).quote
		self.limit = limit
		self.count = count
		self._pages = ''
		self.bing = 'bing.com'

	def run_crawl(self):
		set_page = lambda x: x*11
		urls = [f"https://{self.bing}/search?q={self.q}&count={self.count}&first={set_page(i)}" for i in range(1, self.limit+1)]
		max_attempt = len(urls)
		for url in range(max_attempt):
			self.framework.verbose(f"[BING] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url], allow_redirects=True)
			except:
				self.framework.error('[BING] ConnectionError')
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Bing is missed!')
					break
			else:
				page = req.text
				if '<div class="sw_next">Next</div>' not in page:
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
	def sites(self):
		return self.framework.page_parse(self._pages).sites

	@property
	def links(self):
		parser = self.framework.page_parse(self._pages)
		parser.pclean
		return parser.findall(r'<a href="([^"]+)" h="ID=SERP,[\d\.]+">')

	@property
	def links_with_title(self):
		parser = self.framework.page_parse(self._pages)
		parser.pclean
		links = parser.findall(r'<a href="([^"]+)" h="ID=SERP,[\d\.]+">([^<]+){1,150}</a>')
		links = [x for x in links if x[0].startswith('http')]
		return links

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.links)
