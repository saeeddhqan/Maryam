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
import concurrent.futures

class main:
	def __init__(self, q, limit=1, count=10):
		""" pastebin link
		q       : The query
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
		self._links_and_titles = []
		self.q_formats = {
			'default_q': f'site:pastebin.com "{self.q}"',
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
		self._pages += attr.pages
		self._pastebin_pages = ''

	def open_pages(self, link):
		heading = re.search(r"pastebin\.com/([\w\d]+)", link)
		title = 'no title'
		if heading:
			head_raw = f"https://pastebin.com/raw/{heading.group(1)}"
			try:
				head_req = self.framework.request(url=head_raw).text
			except Exception as e:
				self.framework.verbose('Pastebin is missed!')
			else:
				head_title = f"{self.q} pastes {head_req.splitlines()[0].lstrip()[:30]}...".ljust(10, ' ')
				title = head_title.title()
				self._pastebin_pages += head_req
				self._links_and_titles.append([link, title])

	def run_crawl(self):
		self.framework.thread(self.search, self.thread, self.sources, self.q, self.q_formats, self.limit, self.count, self.sources)
		links = list(set(self.framework.reglib(self._pages).search(r"https://pastebin\.com/[\w\d]{2,}")))
		self.framework.verbose('Rearranging paste links [give it a few seconds]...')
		with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
			[executor.submit(self.open_pages, url) for url in links]

	@property
	def pages(self):
		return self._pastebin_pages

	@property
	def links(self):
		return self._links

	@property
	def links_and_titles(self):
		return self._links_and_titles

	@property
	def dns(self):
		return self.framework.page_parse(self._pastebin_pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pastebin_pages).get_emails(self.q)
