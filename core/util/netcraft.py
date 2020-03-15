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

import hashlib
import re
import urllib

class main:

	def __init__(self, framework, q):
		self.framework = framework
		self.q = q
		self.base_url = 'https://searchdns.netcraft.com/?restriction=site+ends+with&host=' + q
		self._pages = ""

	def request(self, url, cookies=None):
		cookies = cookies or {}
		try:
			req = self.framework.request(url=url)
		except Exception as e:
			self.framework.error(str(e.args))
			self.framework.error("netcraft is missed!")
			return None
		else:
			return req

	def get_next(self, resp):
		link_regx = re.compile(r'<A href="(.*?)"><b>Next page</b></a>')
		link = link_regx.findall(resp)[0]
		url = 'https://searchdns.netcraft.com' + link.replace(" ", "%20")
		return url

	def get_cookies(self, headers):
		if 'set-cookie' in headers:
			cookie = headers['set-cookie']
			cookies = {}
			cookies_list = cookie[0:cookie.find(';')].split("=")
			cookies[cookies_list[0]] = cookies_list[1]
			cookies['netcraft_js_verification_response'] = hashlib.sha1(
				urllib.unquote(cookies_list[1]).encode('utf-8')).hexdigest()
		else:
			cookies = {}
		return cookies

	def run_crawl(self):
		start_url = self.base_url
		resp = self.request(start_url)
		if resp is None:
			return
		cookies = self.get_cookies(resp.headers)
		while True:
			resp = self.request(self.base_url, cookies).text
			self._pages += resp
			if 'Next page' not in resp or resp is None:
				break
			self.base_url = self.get_next(resp)

	@property
	def pages(self):
		return self._pages

	@property
	def dns(self):
		dns = self.framework.page_parse(str(self._pages)).get_dns(self.q)
		return dns
