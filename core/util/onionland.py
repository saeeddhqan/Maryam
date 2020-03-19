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

import re

class main:

	def __init__(self, framework, q, limit):
		self.framework = framework
		self.q = self.framework.urlib(q).quote
		self.limit = 20 if limit > 20 else limit
		self._pages = ''
		self._links = []
		self.onionlandsearchengine = "onionlandsearchengine.com"

	def run_crawl(self):
		urls = ["https://%s/search?q=%s&page=%d" % (self.onionlandsearchengine, self.q, i) for i in range(1, self.limit)]
		max_attempt = len(urls)
		plen = 0
		for i in range(max_attempt):
			try:
				req = self.framework.request(url=urls[i])
			except Exception as e:
				self.framework.error(str(e.args))
				max_attempt -= 1
				if max_attempt == 0:
					self.framework.error("onionland is missed!")
					break
			else:
				self._pages += req.text
				if plen == 0:
					plen = len(self.framework.reglib(self._pages).search("class=\"page\""))
				if plen-1 == i:
					return

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		self._links = [x.replace("</span>\n", "") for x in self.framework.reglib(self._pages).search(r"</span>\n(http?://[^\n]+)")]
		self._links.extend([x.replace("class=\"link\">\n", "") for x in self.framework.reglib(self._pages).search(r"class=\"link\">\n(http?://[^\n]+)")])
		return self._links
	