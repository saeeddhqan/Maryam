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

	def __init__(self, framework, q, key, limit):
		self.framework = framework
		self.q = q
		self.limit = limit
		self.key = key
		self._pages = ""
		self._json_pages = ""
		self.hunter_api = "https://api.hunter.io/v2/domain-search?domain=%s&api_key=%s&limit=%d" \
			%(self.q, self.key, self.limit)

	def run_crawl(self):
		try:
			req = self.framework.request(self.hunter_api)
		except Exception as e:
			self.framework.error(str(e.args))
			self.framework.error("hunter is missed!")
		else:
			self._pages = req.text
			self._json_pages = req.json

	@property
	def pages(self):
		return self._pages
	
	@property
	def json_pages(self):
		return self._json_pages

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)
