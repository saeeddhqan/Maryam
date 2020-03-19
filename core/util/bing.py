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

class main:

	def __init__(self, framework, q, limit, count):
		self.framework = framework
		self.q = self.framework.urlib(q).quote
		self.limit = 20 if limit > 20 else limit
		self.count = count
		self._pages = ""
		self.bing = "bing.com"

	def run_crawl(self):
		urls = ["https://%s/search?q=%s&count=%d&first=1%d" % (
			self.bing, self.q, self.count, i*11) for i in range(0, self.limit)]
		max_attempt = len(urls)
		for url in urls:
			try:
				req = self.framework.request(url=url)
			except Exception as e:
				self.framework.error(str(e.args))
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error("Bing is missed!")
					break
			else:
				page = req.text
				if "<div class=\"sw_next\">Next</div>" not in page:
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
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q)
