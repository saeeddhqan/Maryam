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
		""" pastebin link

		q       : The query domain
		limit   : Number of pages
		"""
		self.framework = main.framework
		self.agent = 'Mozilla/5.0 (Linux; Android 5.1; AFTS Build/LMY47O) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/41.99900.2250.0242 Safari/537.36'
		self.q = q
		self.query = f'site:pastebin.com "{self.q}"'
		self._pages = ''
		self.bing = 'bing.com'
		self.ask = 'www.ask.com'
		self._domains = []
		self.extract_url = 'https://pastebin.com/raw'
		self.limit = limit
		self.count = count
		self._links = []

	def run_crawl(self):
		set_page = lambda x: x*11
		url_b = [f"https://www.{self.bing}/search?q={self.query}&count={self.count}&\
					first={set_page(i)}&form=QBLH&pq={self.query.lower()}" for i in range(1, self.limit+1)]
		url_a = [f"https://{self.ask}/web?q={self.query}&page={i}" for i in range(1, self.limit+1)]
		max_attempt_b = len(url_b)
		max_attempt_a = len(url_a)
		self.framework.verbose(f"[PASTEBIN] Searching inside pastes...")
		try:
			for url in range(max_attempt_b):
				req_b = self.framework.request(url=url_b[url], allow_redirects=True)
			for url in range(max_attempt_a):
				req_a = self.framework.request(url=url_a[url])
		except:
			self.framework.error('[PASTEBIN] ConnectionError')
			max_attempt -= 1
			if max_attempt == 0:
				self.framework.error('Error. Try again!')
		else:
			page = req_b.text
			if 'title="Next page"' not in page:
				self._pages += page
			self._pages += page
			page = req_a.text
			if '>Next</li>' not in page:
				self._pages += page
			self._pages += page
		parser = self.framework.page_parse(self._pages)
		parser.pclean
		links = parser.findall(r'<a target="_blank" href="([^"]+)" h="ID=SERP,[\d\.]+">')
		if len(links) <= 1:
			links += parser.findall(r'<a href="([^"]+)" h="ID=SERP,[\d\.]+">')
		links = [x for x in links if "http://www.microsofttranslator.com" not in x]

	@property
	def pages(self):
		return self._pages

	@property
	def links(self, paste):
		return self._links

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)
