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
import hashlib
import html
from bs4 import BeautifulSoup as bs

class main:

		def __init__(self, num):
			""" numverify search engine
					num     : number to search
			"""
			self.framework = main.framework
			self.num = num
			self._json = ''
			self._suffix = ''
			self.numverify = 'https://numverify.com'

		def forge_secret(self):
			# Numverify uses AJAX with an insecure hash to verify its requests
			# A secret value from a tag is appended to the phone number and md5'd 
			return hashlib.md5((self.num+self._suffix).encode()).hexdigest()

		def run_crawl(self):
			self.framework.verbose('Searching...')
			self.num = re.sub(r'\+|\s', '', self.num);
			try:
				req = self.framework.request(url=self.numverify)
				soup = bs(req.text,'html.parser')

				self._suffix = soup.find('input', {'name': 'scl_request_secret'})['value']
				secret = self.forge_secret()
				url = ''.join([f'{self.numverify}/php_helper_scripts/phone_api.php',
					f'?secret_key={secret}&number={self.num}'])

				req = self.framework.request(url=url)
				self._json = req.json()
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/numverify', 'run_crawl')
				self.framework.error('Numverify is missed!', 'util/numverify', 'run_crawl')
				return

		@property
		def json(self):
			return self._json
