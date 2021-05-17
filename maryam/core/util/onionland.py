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
		""" use onionlandsearchengine.com

			q 		  : Query for search
			limit	  : Number of pages
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self.limit = 20 if limit > 20 else limit
		self._pages = ''
		self._links = []
		self.onionlandsearchengine = 'onionlandsearchengine.com'

	def run_crawl(self):
		urls = [f"https://{self.onionlandsearchengine}/search?q={self.q}&page={i}" for i in range(1, self.limit)]
		max_attempt = len(urls)
		plen = 0
		for url in range(max_attempt):
			self.framework.debug(f'[ONIONLAND] Searching in {url} page...')
			try:
				req = self.framework.request(url=urls[url])
			except:
				self.framework.print_exception()
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Onionland is missed!', 'util/onionland', 'run_crawl')
					break
			else:
				self._pages += req.text
				if plen == 0:
					plen = len(self.framework.reglib(self._pages).search('class="page"'))
				if plen-1 == url:
					return

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		self._links = [x.replace('</span>\n', '') for x in self.framework.reglib(self._pages).search(r'</span>\n(https?://.*)')]
		self._links.extend([x.replace('class="link">\n', '') for x in self.framework.reglib(self._pages).search(r'class="link">\n(https?://.*)')])
		return self._links
