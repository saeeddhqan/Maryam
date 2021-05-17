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
		self.q = q.split('_')[0]
		self._pages = ''
		self.sources = ['google', 'bing', 'yahoo', 'ask', 'carrot2', 'duckduckgo', 'millionshort', 'qwant']
		self._domains = []
		self.extract_url = 'https://pastebin.com/raw'
		self.limit = limit
		self.count = count
		self.thread = 3
		self._links = []
		self.q_formats = {
			'default_q': f'site:pastebin.com "{self.q}"',
			'yippy_q': f'"pastebin.com" {self.q}',
			'qwant_q': f'site:pastebin.com {self.q}'
		}
		

	def search(self, self2, name, q, q_formats, limit, count):
		engine = getattr(self.framework, name)
		q = self.q_formats[f"{name}_q"] if f"{name}_q" in self.q_formats else self.q_formats['default_q']
		varnames = engine.__init__.__code__.co_varnames
		if 'limit' in varnames and 'count' in varnames:
			attr = engine(q, limit, count)
		elif 'limit' in varnames:
			attr = engine(q, limit)
		else:
			attr = engine(q)

		attr.run_crawl()
		self._links += attr.links
		self._pages += attr.pages

	def run_crawl(self):
		self.framework.thread(self.search, self.thread, self.sources, self.q, self.q_formats, self.limit, self.count, self.sources)

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
