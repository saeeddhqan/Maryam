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

	def __init__(self, q, limit=2):
		""" startpage.com search engine

			q 		  : Query for search
			limit	  : Number of pages
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self.limit = limit
		self._pages = ''
		self.startpage = 'startpage.com'

	def run_crawl(self):
		urls = [f"https://{self.startpage}/sp/search?query={self.q}&page={i}" for i in range(1, self.limit+1)]
		max_attempt = len(urls)
		for url in range(len(urls)):
			self.framework.verbose(f"[STARTPAGE] Searching in {url} page...")
			try:
				req = self.framework.request(url=urls[url])
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/startpage', 'run_crawl')
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error('Startpage is missed!', 'util/startpage', 'run_crawl')
					break
			else:
				page = req.text
				if '> Next <' not in page:
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
