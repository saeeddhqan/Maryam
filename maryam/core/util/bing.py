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

	def __init__(self, q, limit=1, count=10):
		""" bing.com search engine
			
			q         : Query for search
			limit	  : Number of pages
			count	  : Number of links
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self.limit = limit
		self.count = count
		self._pages = ''
		self.bing = 'bing.com'

	def run_crawl(self):
		set_page = lambda x: x*11
		urls = [f"https://www.{self.bing}/search?q={self.q}&count={self.count}&\
					first={set_page(i)}&form=QBLH&pq={self.q.lower()}" for i in range(1, self.limit+1)]
		max_attempt = len(urls)
		for url in range(max_attempt):
			self.framework.verbose(f"[BING] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url], allow_redirects=True)
			except:
				self.framework.error('ConnectionError', 'util/bing', 'run_crawl')
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Bing is missed!', 'util/bing', 'run_crawl')
					break
			else:
				page = req.text
				if 'title="Next page"' not in page:
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
		links = parser.findall(r'<a target="_blank" href="([^"]+)" h="ID=SERP,[\d\.]+">')
		if len(links) <= 1:
			links += parser.findall(r'<a href="([^"]+)" h="ID=SERP,[\d\.]+">')
		links = [x for x in links if "http://www.microsofttranslator.com" not in x]
		return links

	@property
	def links_with_title(self):
		parser = self.framework.page_parse(self._pages)
		parser.pclean
		links = parser.findall(r'<a target="_blank" href="([^"]+)" h="ID=SERP,[\d\.]+">([^<]+)</a>')
		if len(links) <= 1:
			links = parser.findall(r'<a href="([^"]+)" h="ID=SERP,[\d\.]+">([^<]+)</a>')
		links = [x for x in links if x[0].startswith('http') and\
			"http://www.microsofttranslator.com" not in x[0] and\
			"Translate this page" not in x[1]]
		return links

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
