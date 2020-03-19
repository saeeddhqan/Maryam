# -*- coding : u8 -*-
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

	def __init__(self, framework, page):
		self.framework = framework
		self.page = page

	def pclean(self):
		subs = r"<em>|<b>|</b>|</em>|<strong>|</strong>|<wbr>|</wbr>|<span class=\"vivbold qt0\">|%22"
		self.page = re.sub(subs, "", self.page)
		self.page = re.sub(r"%3a", ' ', self.page)
		self.page = re.sub(r"%2f", ' ', self.page)
		self.page = re.sub(r"%2f", ' ', self.page)

	def dork_clean(self, host):
		# Clear Dork's footprints
		host = re.sub(r"([\'\"]+)|(%40|@)", "", host)
		return host

	def findall(self, reg):
		return re.compile(reg).findall(self.page)

	@property
	def sites(self):
		self.pclean()
		reg = re.compile(r"<cite>(.*?)</cite>")
		resp = []
		for i in reg.findall(self.page):
			if i not in resp:
				resp.append(i)
		return resp
		
	@property
	def social_nets(self):
		self.pclean()
		reg_id = self.framework.reglib().social_network_ulinks
		resp = {}
		for i in reg_id:
			name = re.findall(reg_id[i], self.page)
			names = []
			for j in name:
				if j not in names:
					names.append(j)
			resp[i] = names
		return resp

	def get_emails(self, host):
		self.pclean()
		host = self.dork_clean(host + '.' if '.' not in host else host)
		resp = []
		for i in re.findall(r"[A-z0-9.\-]+@[A-z0-9\-\.]{0,255}?%s(?:[A-z]+)?" % host, self.page):
			if i not in resp:
				resp.append(i)
		return resp

	@property
	def all_emails(self):
		self.pclean()
		emails = self.framework.reglib(self.page).emails
		return emails

	def get_dns(self, host):
		self.pclean()
		resp = []
		reg = r"[A-z0-9\.\-%s]+\.%s" % ('%',host.replace("\"","").replace("'",""))
		for i in re.findall(reg, self.page):
			i = i.replace("\\", "").replace("www.", "")
			if i not in resp and "%" not in resp:
				resp.append(i)

		return resp

	def get_docs(self, query, urls=None):
		self.pclean()
		if "%" in query:
			query = self.framework.urlib(query).unquote
		ext = re.search(r"filetype:([A-z0-9]+)", query)
		if ext:
			docs = []
			ext = ext.group(1)
			if urls is None:
				# Concat url_m regex with file extentions
				reg = "%s.%s" % (self.framework.reglib(self.page).url_m, ext)
				docs = self.findall(reg)
			else:
				for url in urls:
					if url.endswith("."+ext):
						docs.append(url)
			return list(set(docs))
		else:
			self.framework.error("Filetype not specified. Concat 'filetype:doc' to the query")
			return []
