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
import re

class main:

	def __init__(self, framework, q):
		self.framework = framework
		self.q = q
		self._pages = ''
		self._links = []
		self.yippy = "yippy.com"

	def run_crawl(self):
		reg = r"<a href=\"(https://?[^\"]+)\" class=\"title\""
		geturl = "http://%s/search?query=%s" % (self.yippy, self.q)
		req = self.framework.request(url=geturl)
		txt = req.text
		self._links = [x.replace("<a href=\"","") for x in re.findall(reg, txt)]
		self._pages = txt
		root = re.search(r"(root-[\d]+-[\d]+%7C[\d]+)\">next</",txt)
		if root:
			root = root.group()
			file = re.search(r"%3afile=([A-z0-9_\-\.]+)&amp",txt)
			if not file:
				self.framework.error("yippy is missed!")
				return
			file = file.group()
			root = re.sub(r"[\d]+-[\d]+", "0-8000", root)
			newurl = "https://yippy.com/ysa/cgi-bin/query-meta?v%s;v:state=root|%s"%(file,root.replace("\">next</",""))
			req = self.framework.request(url=newurl)
			self._pages += req.text
			self._links.extend([x.replace("<a href=\"","").replace(" class=\"title\"","") for x in re.findall(reg, self._pages)])
				
	@property
	def pages(self):
		return self._pages

	@property
	def links(self):
		return self._links
	
	@property
	def dns(self):
		return self.framework.page_parse(self._pages).get_dns(self.q)

	@property
	def emails(self):
		return self.framework.page_parse(self._pages).get_emails(self.q)

	@property
	def docs(self):
		return self.framework.page_parse(self._pages).get_docs(self.q)
