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

	def __init__(self, q, limit=2):
		""" netcraft.com for find dns

			q 		  : Query for search
		"""
		self.framework = main.framework
		self.q = q
		self.limit = limit
		self.base_url = f"https://www.virustotal.com/ui/domains/{q}/subdomains?relationships=resolutions&cursor=STMwCi4=&limit=40"
		self._pages = ''

	def request(self, url):
		try:
			req = self.framework.request(url=url)
		except:
			self.framework.error('[VIRUSTOTAL] ConnectionError')
			self.framework.error('VirusTotal is missed!')
			return False
		return req

	def run_crawl(self):
		count = 0
		while True:
			self.framework.verbose(f"[VIRUSTOTAL] Searching in {count} page...")
			req = self.request(self.base_url)
			if not req:
				return
			self._pages += req.text
			json = req.json()
			if count+1 == self.limit:
				break
			if 'links' in json:
				if 'next' in json['links']:
					self.base_url = json['links']['next']
				else:
					return
			else:
				return
			count += 1

	@property
	def pages(self):
		return self._pages

	@property
	def dns(self):
		resp = []
		parser = self.framework.page_parse(str(self._pages)).get_dns(self.q)
		for host in list(set(parser)):
			if host[0].isdigit():
				matches = re.match(r".+([0-9])[^0-9]*$", host)
				host = host[matches.start(1) + 1:]
			if host.startswith('.'):
				host = host[1:]
			resp.append(host)
		return resp
