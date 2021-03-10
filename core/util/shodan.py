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
from shodan import Shodan
import json
class main:

#	def __init__(self, framework, q, key, count=10):
	def __init__(self, framework, q, key, host):
		""" shodan.io search engine

			framework  : core attribute
			q          : query for search
			key		   : API key
			host	   : Returns all services that have been found on the given host IP
		"""
		self.framework = framework
		self.q = q
		self.api_key = key
		self.host = host
#		self.shodan_api = f"https://api.shodan.io/shodan/host/search?key={self.key}&query={self.q}"
		self._links = []
	def run_crawl(self):
		self.framework.verbose('[SHODAN] Searching in shodan...')
		try:
			if self.host is None:
				req = Shodan(self.api_key).search(self.q)
#				req = self.framework.request(self.shodan_api)
				for results in req['matches']:
					result_list = {key: results[key] for key in results.keys() & {'location', 'org','ip_str','port','hostnames'}}
					self._links = req
					print(json.dumps(result_list, separators=(',', ':'), indent=4))
				return
			else:
				req = Shodan(self.api_key).host(self.host)
				self._links = req
				print(json.dumps(req, separators=(',', ':'), indent=4))
				return
		except Exception as e:
			self.framework.error(f"[SHODAN]:{e}")
			self.framework.debug('[SHODAN] ConnectionError')
			return

	@property                                                                                                                      
	def links(self):
		return self._links

