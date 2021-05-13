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

	def __init__(self, q):
		""" crt.sh search engine

			q 		  : Query for search
		"""
		self.framework = main.framework
		self.q = q
		self._pages = ''
		self._json_page = ''
		self.crt = f"https://crt.sh/?q={q}&output=json"

	def run_crawl(self):
		self.framework.verbose('[CRT] Starting Search...')
		try:
			req = self.framework.request(self.crt)
		except:
			self.framework.debug('[CRT] ConnectionError')
			self.framework.error('CRT is missed!', 'util/crt', 'run_crawl')
			return
		self._pages = req.text
		try:
			self._json_page = req.json()
			if self._json_page == []:
				self._json_page = {}
		except:
			self.framework.error('CRT is missed!')
			self._json_page = []

	@property
	def pages(self):
		return self._pages
	
	@property
	def json_page(self):
		return self._json_page

	@property
	def dns(self):
		return self.framework.page_parse(self.pages).get_dns(self.q)
