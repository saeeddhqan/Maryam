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
		self.q = self.framework.urlib(q).quote()
		self._pages = ""
		self.mailshunt = "mailshunt.com"

	def run_crawl(self):
		url = "http://%s/domain-search/" % (self.mailshunt)
		self.q = self.framework.urlib(self.q).netloc
		try:
			header = self.framework.request(url=url).headers["Set-cookie"]
			req = self.framework.request(url,
				method="POST",
				payload={"domain" : self.q}
				)
		except Exception as e:
			self.framework.error(str(e.args))
			self.framework.error("mailshunt is missed!")
		else:
			self._pages += req.text

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)
