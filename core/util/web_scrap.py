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

from lxml.html import fromstring
import re
# Web Scraper v4.4

class main:

	def __init__(self, framework, url, force, debug=False, limit=20):
		self.framework = framework
		# ADD http:// 
		self.url = self.framework.urlib(url).sub_service(serv="http")
		self.urlib = self.framework.urlib
		self.force = force
		self.debug = debug
		self.limit = limit
		self._category_pages = {}
		self._pages = ''
		self._links = []
		self._external_links = []
		self._query_links = []
		self._phones = []
		self._css = []
		self._js = []
		self._cdn = []
		self._comments = []
		self._emails = []
		self._social_nets = {}
		self.numerator = 0

	def run_crawl(self):
		final_links = []

		# If key not in links append it
		def rept(key, _list):
			if type(key) is list:
				for i in key:
					if str(i) not in _list:
						_list.append(i)
			else:
				if key not in _list:
					_list.append(key)
			return _list

		def debug(val):
			if self.debug:
				self.framework.output(val)

		def add_cdn(link):
			cond = link[:2] == "//" and '.' in link and link not in self._cdn
			if cond:
				rept(link, self._cdn)
				return True

		def add_phone(link):
			cond = link[:6] == "tel://"
			if cond:
				rept(link, self._phones)
				return True

		def add_email(link):
			cond = link.startswith("mailto:")
			if cond:
				rept(link[6:], self._emails)
				return True

		def cleaner(url, baseurl):
			url = unicode(url)
			# ADD slash to end url
			url2 = baseurl+'/' if not baseurl.endswith("/") else baseurl
			urparse = self.urlib(url)
			urparse.url = urparse.quote if '%' not in url else url
			urparse2 = self.urlib(url2)
			cond1 = url in ("%20", '', '/', "%23", "#")
			cond2 = len(
				urparse.url) > 1 and "%3a//" not in urparse.url.lower() and urparse.url[:2] != "//"
			cond3 = urparse.url[:2] == "//"
			if cond1:
				return False
			elif cond2:
				url = url[1:] if url[0] == '/' else url
				urparse.url = urparse2.join(url)
			elif cond3:
				urparse.url = url
			else:
				urparse.url = url
			url = urparse.url+'/' if not urparse.url.endswith("/") else urparse.url
			return url

		self.url = cleaner(self.url, self.url)

		# Get Data from URL and parse it
		def get_source(url, baseurl):
			self.numerator += 1
			links = []
			# Send Request
			try:
				req = self.framework.request(url=url)
			except Exception as e:
				return False
			else:
				if req.status_code not in [200, 204]:
					return False
				else:
					resp = req.text
			pp = self.framework.page_parse(resp)
			# Add social nets
			for i in pp.social_nets:
				if i not in self._social_nets:
					self._social_nets[i] = pp.social_nets[i]
				else:
					self._social_nets[i] = rept(pp.social_nets[i], self._social_nets[i])
			# Add emails
			self._emails = rept(pp.all_emails, self._emails)
			del pp
			tree = fromstring(resp)

			# ADD Comments
			html_comments = re.findall(r"<!--(.*?)-->", resp)
			js_comments = re.findall(r"/\*(.*?)\*/", resp)
			html_comments.extend(js_comments)
			self._comments = rept(html_comments, self._comments)

			# ADD JS and CSS files
			get_js = tree.xpath("//script/@src")
			get_css = tree.xpath("//link/@href")
			for i in get_js:
				if i.endswith(".js"):
					i = cleaner(i, baseurl)
					if i:
						debug(i)
						add_cdn(i)
						rept(i, self._js)

			for i in get_css:
				if i.endswith(".css"):
					i = cleaner(i, baseurl)
					if i:
						debug(i)
						add_cdn(i)
						rept(i, self._css)

			get_a = tree.xpath('//a/@href')

			for i in get_a:
				# join url
				i = cleaner(i, baseurl)
				if not i:
					continue
				debug(i)
				# ADD CDN link and Phone number
				if add_cdn(i) or add_phone(i) or add_email(i):
					continue
				urparse = self.urlib(i)
				# If the link is external link, append it to self._external..
				if urparse.netroot.lower() not in self.url.lower():
					rept(i, self._external_links)
					continue

				# If the link is query link, append it to self._query..
				if urparse.query != "":
					rept(str(i), self._query_links)
		
				# At the end, append link to links and ..
				rept(i, links)
				rept(i, final_links)

			if resp != "":
				self._pages = self._pages + resp
				self._category_pages[url] = resp
			return links

		lnks = get_source(self.url, self.url)
		# If no lnks return just input url
		if not lnks:
			return [self.url]
		else:
			final_links = rept(self.url, final_links)

		if not self.force and self.limit == 1:
			self._links = final_links
			return
			
		for i in lnks:
			lnks1 = get_source(i, i)
			if self.numerator == self.limit:
				self._links = final_links
				return
			if not lnks1:
				continue
			for j in lnks1:
				lnks2 = get_source(j, i)
				if self.numerator == self.limit:
					self._links = final_links
					return
				if not lnks2:
					continue
				for k in lnks2:
					lnks3 = get_source(k, j)
					if self.numerator == self.limit:
						self._links = final_links
						return
					if not lnks3:
						continue
		self._links = final_links

	@property
	def pages(self):
		return self._pages

	@property
	def category_pages(self):
		return self._category_pages

	@property
	def links(self):
		return self._links

	@property
	def external_links(self):
		return self._external_links

	@property
	def query_links(self):
		return self._query_links

	@property
	def js(self):
		return self._js

	@property
	def css(self):
		return self._css

	@property
	def cdn(self):
		return self._cdn

	@property
	def phones(self):
		return self._phones

	@property
	def comments(self):
		return self._comments

	@property
	def emails(self):
		return self._emails
	
	@property
	def social_nets(self):
		return self._social_nets
