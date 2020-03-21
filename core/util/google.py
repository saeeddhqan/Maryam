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
import tempfile
import webbrowser

class main:

	def __init__(self, framework, q, limit, count):
		self.framework = framework
		self.q = self.framework.urlib(q).quote
		self.agent = framework.rand_uagent().lynx[0]
		self._pages = ""
		self.limit = limit
		# count links in page
		self.num = count
		self._links = []

	def run_crawl(self):
		page = 1
		url = "http://google.com/search"
		payload = {"num" : self.num, "start" : page, "ie" : "utf-8", "oe" : "utf-8", "q" : self.q}
		max_attempt = 0
		while True:
			try:
				req = self.framework.request(
					url=url,
					payload=payload,
					redirect=False,
					agent=self.agent)
			except Exception as e:
				self.framework.error(e)
			else:
				if req.status_code == 503:
					req = self.captcha(req)
					continue
				if req.status_code in [301, 302]:
					redirect = req.headers["location"]
					req = self.framework.request(url=redirect, redirect=False, agent=self.agent)
				self._pages += req.text
				page+=1
				if self.limit == page:
					break

	def captcha(self, resp):
		# set up the captcha page markup for parsing
		tree = fromstring(resp.text)
		# extract and request the captcha image
		resp = self.framework.request('https://ipv4.google.com' + tree.xpath('//img/@src')[0], redirect=False, agent=self.agent)
		# store the captcha image to the file system
		with tempfile.NamedTemporaryFile(suffix='.jpg') as fp:
			fp.write(resp.raw)
			fp.flush()
			# open the captcha image for viewing in gui environments
			w = webbrowser.get()
			w.open('file://' + fp.name)
			self.framework.alert(fp.name)
			try:
				_payload = {'captcha': raw_input('[CAPTCHA] Answer: ')}
			except:
				_payload = {'captcha': input('[CAPTCHA] Answer: ')}
			# temporary captcha file removed on close
		# extract the form elements for the capctah answer request
		form = tree.xpath('//form[@action="index"]')[0]
		for x in ['q', 'continue', 'submit']:
			_payload[x] = form.xpath('//input[@name="%s"]/@value' % (x))[0]
		# send the captcha answer
		return self.framework.request('https://ipv4.google.com/sorry/index', payload=_payload, agent=self.agent)

	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		try:
			tree = fromstring(self._pages)
		except:
			return self._links
		else:
			links = tree.xpath("//a/@href")
			for link in links:
				cond1 = re.compile(r"/url\?q=[^/]").match(link) != None
				cond2 = "http://webcache.googleusercontent.com" not in link
				cond3 = link not in self._links
				if cond1 and cond2 and cond3:
					link = re.sub(r"/url\?q=", "", link)
					self._links.append(link)
			return self._links

	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q, self.get_links)
