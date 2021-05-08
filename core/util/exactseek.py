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
		"""
		photon uses osm data for locations and reverse geolocation
		q       :   query
		"""
		self.q = q
		self.framework = main.framework
		self._pages = ''
		self._json = {}
		self.ex = 'https://www.exactseek.com/cgi-bin/search.cgi'

	def run_crawl(self):
		self.framework.verbose("[EXACTSEEK]Searching in exactseek.com...")
		url = f"{self.ex}?q={self.q}"
		max_page = 1
		page_no = 0
		while(int(max_page) > int(page_no)):
			try:
				req = self.framework.request(
					url = url,
					params = {'s':f'{page_no}1'}
				)
				try:
					total = re.findall(r';s=(\d*)1',req.text)
					max_page = total[-1]
				except:
					max_page = 0
				else:
					page_no += 1
				print(req.url)
				print(total)
				print(max_page)
			except:
				self.framework.error('ConnectionError', 'util/exactseek', 'run_crawl')
			else:
				result = req.text.split('<!-- Begin Search Results -->')[1].split('<!-- End Search Results -->')[0]
				self._pages = result

	@property
	def pages(self):
		return self._pages
	@property
	def json(self):
		return self._json