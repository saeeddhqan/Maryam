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

from hashlib import sha1
import re

class main:

	def __init__(self, q, limit=4):
		""" netcraft.com for find dns

			q 		  : Query for search
		"""
		self.framework = main.framework
		self.q = q
		self.limit = limit
		self.base_url = f"https://searchdns.netcraft.com/?restriction=site+ends+with&host={q}"
		self._pages = ''

	def request(self, url, cookies=None):
		cookies = cookies or {}
		try:
			req = self.framework.request(url=url, cookies=cookies)
		except Exception as e:
			self.framework.error(f"ConnectionError {e}.", 'util/netcraft', 'request')
			self.framework.error('Netcraft is missed!', 'util/netcraft', 'request')
			return False
		return req

	def get_next(self, resp):
		link_regx = re.compile(r'<a class="btn-info" href="(.*?)">Next Page <i')
		link = link_regx.findall(resp)
		if not link:
			return False
		link = link[0]

		url = 'https://searchdns.netcraft.com' + link.replace(' ', '%20')
		return url

	def get_cookies(self, headers):
		if 'set-cookie' in headers:
			cookie = headers['set-cookie']
			cookies = {}
			cookies_list = cookie[0:cookie.find(';')].split('=')
			cookies[cookies_list[0]] = cookies_list[1]
			cookies['netcraft_js_verification_response'] = sha1(
				self.framework.urlib(cookies_list[1]).unquote.encode('utf-8')).hexdigest()
		else:
			cookies = {}
		return cookies

	def run_crawl(self):
		start_url = self.base_url
		resp = self.request(start_url)
		if not resp:
			return
		count = 1
		cookies = self.get_cookies(resp.headers)

		while True:
			self.framework.verbose(f"[NETCRAFT] Searching in {count} page...")
			resp = self.request(self.base_url, cookies).text
			if not resp:
				return
			self._pages += resp
			if count+1 == self.limit:
				break
			next_link = self.get_next(resp)
			if not next_link:
				return
			self.base_url = next_link
			count += 1

	@property
	def pages(self):
		return self._pages

	@property
	def dns(self):
		dns = self.framework.page_parse(str(self._pages)).get_dns(self.q)
		return dns
