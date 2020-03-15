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
		"name": "Email Searcher",
		"author": "Saeeddqn",
		"version": "0.3",
		"description": "Search in search engines for find emails. engines[bing,google,yahoo,yandex,metacrawler,ask,baidu,startpage,hunter]",
		"options": (
			("query", BaseModule._global_options["target"], True, "Domain Name, Company Name, etc", "-q", "store"),
			("limit", 3, False, "Search limit", "-l", "store"),
			("count", 50, False, "Links count in page(min=10, max=100)", "-c", "store"),
			("engines", "google,metacrawler", True, "Search engine names. e.g bing,google,..", "-e", "store"),
			("key", None, False, "hunter.io api key", "-k", "store"),
			("output", False, False, "Save output to  workspace", "--output", "store_false"),
		),
		"examples": ["email_search -n microsoft -e google,bing,yahoo -l 3 --output", "email_search -n microsoft.com -e metacrawler --output"]
	}

	def module_run(self):
		name = self.options["query"].replace("@", "")
		limit = self.options["limit"]
		count = self.options["count"]
		engines = self.options["engines"].split(",")
		q = "\"@%s\"" % name
		wled = {}

		if "google" in engines:
			search = self.google(name, limit, count)
			search.run_crawl()
			wled["google"] = search.emails

		if "bing" in engines:
			search = self.bing(name, limit, count)
			search.run_crawl()
			wled["bing"] = search.emails

		if "yahoo" in engines:
			search = self.yahoo(name, limit, count)
			search.run_crawl()
			wled["yahoo"] = search.emails

		if "metacrawler" in engines:
			search = self.metacrawler(name, limit)
			search.run_crawl()
			wled["metacrawler"] = search.emails

		if "yandex" in engines:
			search = self.yandex(name, limit, count)
			search.run_crawl()
			wled["yandex"] = search.emails

		if "startpage" in engines:
			search = self.startpage(name, limit)
			search.run_crawl()
			wled["startpage"] = search.emails

		if "baidu" in engines:
			search = self.baidu(name, limit)
			search.run_crawl()
			wled["baidu"] = search.emails

		if "netcraft" in engines:
			search = self.netcraft(name)
			search.run_crawl()
			wled["netcraft"] = search.emails

		if "hunter" in engines:
			key = self.options["key"]
			search = self.hunter(name, key)
			search.run_crawl()
			wled["hunter"] = search.emails

		uniq = []
		for eng in wled:
			self.alert(eng)
			for email in wled[eng]:
				if email not in uniq:
					uniq.append(email)
					self.output("\t%s"%email)

		self.save_gather({"emails" : uniq}, "osint/email_search", name, output=self.options["output"])
