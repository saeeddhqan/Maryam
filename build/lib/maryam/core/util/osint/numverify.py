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

import random

class main:

		def __init__(self, num):
			""" numverify search engine
					num		: number to search
					country : country code
					
			"""
			self.framework = main.framework
			self.num = num
			self._json = ''
			self.numverify = 'http://apilayer.net/api/validate'
			self.keys = [
				'3489ab1ab092628f8b2a63b3d94b75f3',
				'ea52c77e9877dd4fdb83bdec925d3eeb',
				'e6f3944b3724f836871a4f9dcc546eb6',
				'3796398e6c96912c29a56ec0177b8d6b',
				'95f0bc6561937986c3386b1ffcd36ae9',
				'd49245f8853efbff4dfd245387531727',
				'62552e99ed3cb92159be4153242b7eea',
				'1322a4a256acd589e2e3ce73e65fdd3f',
				'3fcf94548f2177e781eff270d43790f6',
				'7778341260206c06fac4a2727a27955f',
				'a0bfc16589d513fc472832935c9c6528',
				'3618d844c1b6802106a6309c92c71ac2',
				'376bbc8ef5ee4a9d8f6a81a7ddd9f4cd',
				'd4e8383a4f2efec6e523faad8797c4d1',
				'0a45e3f8273a7f929f4ec237e4f24d10',
				'64edafd9cc5d839d8d9bac9ac0837851',
				'5165b0fec39bb03e42f43d4cc5513dcb',
				'e2a851b9b76a579c0fef4304969546e7',
				'9a39c3058615ec330c7223a596f62934',
				'2a06b63cb88a13ebeea7e5f83f01f8d7',
				'1ed52249226585cdb176926e34d75aa5',
				'8a6cb00cac3c904dd1c82b29ab5061d0',
				'fe11bd5cfea457f9fda5ed3fecc8fc54'
			]

		def run_crawl(self):
			self.framework.verbose('Searching...')
			try:
				payload = { 
						'access_key': random.choice(self.keys),
						'number': self.num,
						'format': 1
				}
				req = self.framework.request(
						url=self.numverify,
						params=payload)
				self._json = req.json()
			except Exception as e:
				self.framework.error(f"ConnectionError {e}.", 'util/numverify', 'run_crawl')
				self.framework.error('Numverify is missed!', 'util/numverify', 'run_crawl')
				return

		@property
		def json(self):
			return self._json
