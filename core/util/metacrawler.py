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

	def __init__(self, framework, q, limit):
		self.framework = framework
		self.q = self.framework.urlib(q).quote
		self.limit = limit
		self._pages = ""
		self.metacrawler = "metacrawler.com"

	def run_crawl(self):
		urls = ["http://%s/serp?q=%s&page=%d" % (
			self.metacrawler, self.q, i) for i in range(0, self.limit)]
		max_attempt = len(urls)
		for url in urls:
			try:
				req = self.framework.request(url=url)
			except Exception as e:
				self.framework.error(str(e.args))
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error("metacrawler is missed!")
					break
			else:
				page = unicode(req.text)
				if ">Next</" not in page:
					self._pages += page
					break
				self._pages += page

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		return self.framework.reglib(self._pages).search(r"<a class=\"web-bing__title\" href=\"([A-z0-9.,:;%/\\?#@$^&*\(\)~\-_+=\"\']+)\"")

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)
	
	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)
	
	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.links)
