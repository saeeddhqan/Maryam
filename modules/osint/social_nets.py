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
from core.module import BaseModule


class Module(BaseModule):

	meta = {
		"name": "Get Usernames in Social Networks",
		"author": "Saeeddqn",
		"version": "0.3",
		"description": "Search for find Usernames in social networks. engines[bing,google,yahoo,yandex,metacrawler,ask,startpage]",
		"options": (
			("name", BaseModule._global_options["target"], True, "Company Name,domain name, .. without <PRTCL>://", "-n", "store"),
			("engines", "google", True, "Search engine names. e.g \"bing,google,..\"", "-e", "store"),
			("limit", 5, False, "Limit for page search", "-l", "store"),
			("count", 100, False, "Links count in page(min=10, max=100)", "-c", "store"),
			("output", False, False, "Save output to  workspace", "--output", "store_false"),
		),
		"examples": ["social_nets -n microsoft -e google,bing,yahoo -c 50 --output", "social_network -n microsoft.com -e google"]

	}

	def module_run(self):
		name = self.options["name"]
		fin = {}
		limit = self.options["limit"]
		engines = self.options["engines"].lower().split(",")
		wled = ""

		if "google" in engines:
			self.alert("Google")
			search = self.google(name, limit, 50)
			search.run_crawl()
			wled += search.pages

		if "bing" in engines:
			self.alert("Bing")
			search = self.bing(name, limit, 50)
			search.run_crawl()
			wled += search.pages

		if "yahoo" in engines:
			self.alert("Yahoo")
			search = self.yahoo(name, limit, 50)
			search.run_crawl()
			wled += search.pages

		if "metacrawler" in engines:
			self.alert("MetaCrawler")
			search = self.metacrawler(name, limit)
			search.run_crawl()
			wled += search.pages

		if "yandex" in engines:
			self.alert("Yandex")
			search = self.yandex(name, limit, 50)
			search.run_crawl()
			wled += search.pages

		if "startpage" in engines:
			self.alert("StartPage")
			search = self.startpage(name, limit)
			search.run_crawl()
			wled += search.pages

		if "baidu" in engines:
			search = self.baidu(name, limit)
			search.run_crawl()
			wled += search.pages

		usernames = self.page_parse(wled).social_nets
		self.alert("Social Networks:")
		for i in usernames:
			if usernames[i] != []:
				for j in usernames[i]:
					self.output("\t\t%s" % str(j), "g")
			else:
				self.output("\t\tunknown")

		self.save_gather(usernames, "osint/dns_search", name, output=self.options["output"])
