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

	def __init__(self, q):
		""" ahmia.fi search engine
			
			q 		  : query for search
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote
		self._pages = ''
		self._links = []
		self.ahmia = 'ahmia.fi'

	def run_crawl(self):
		url = f"https://{self.ahmia}/search/?q={self.q}"
		try:
			req = self.framework.request(url=url)
		except:
			self.framework.print_exception()
			self.framework.error('Ahmia is missed!', 'util/ahmia', 'run_crawl')
		self._pages = req.text
			
	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		return self.framework.page_parse(self._pages).findall(r'redirect_url=(.*?)">')
