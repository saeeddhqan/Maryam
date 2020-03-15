# -*- coding: u8 -*-
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

from lxml.html import fromstring

class main:

	def __init__(self, framework, q, limit):
		self.framework = framework
		self.q = self.framework.urlib(q).quote
		self.limit = limit
		self._pages = ""
		self.startpage = "startpage.com"

	def run_crawl(self):
		urls = ["https://%s/sp/search?query=%s&page=%d" % (self.startpage, self.q, i) for i in range(0, self.limit)]
		print(urls)
		max_attempt = len(urls)
		for url in urls:
			try:
				req = self.framework.request(url=url)
			except Exception as e:
				self.framework.error(str(e.args))
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error("startpage is missed!")
					break
			else:
				page = req.text
				if "> Next <" not in page:
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
		return self.framework.page_parse(self._pages).get_emails(self.query)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.query)
