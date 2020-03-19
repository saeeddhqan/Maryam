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
		"version": "0.5",
		"description": "Search in search engines for find emails.",
		"sources": ("bing", "google", "yahoo", "yandex", "metacrawler", 
					"ask", "baidu", "startpage", "hunter", "yippy"),
		"options": (
			("query", BaseModule._global_options["target"], True, "Domain Name, Company Name, etc", "-q", "store"),
			("limit", 3, False, "Search limit", "-l", "store"),
			("count", 50, False, "Links count in page(min=10, max=100)", "-c", "store"),
			("engines", "google,metacrawler", True, "Search engine names. e.g bing,google,..", "-e", "store"),
			("key", None, False, "hunter.io api key", "-k", "store"),
			("output", False, False, "Save output to  workspace", "--output", "store_false"),
		),
		"examples": ("email_search -q microsoft -e google,bing,yahoo -l 3 --output", "email_search -q microsoft.com -e metacrawler --output")
	}

	def module_run(self):
		name = self.options["query"].replace('@', '')
		limit = self.options["limit"]
		count = self.options["count"]
		engines = self.options["engines"].split(',')
		q = "\"%s40%s\"" % ("%", name)
		emails = []

		if "google" in engines:
			search = self.google(q, limit, count)
			search.run_crawl()
			emails.extend(search.emails)

		if "bing" in engines:
			search = self.bing(q, limit, count)
			search.run_crawl()
			emails.extend(search.emails)

		if "yahoo" in engines:
			search = self.yahoo(q, limit, count)
			search.run_crawl()
			emails.extend(search.emails)

		if "metacrawler" in engines:
			search = self.metacrawler(q, limit)
			search.run_crawl()
			emails.extend(search.emails)

		if "yandex" in engines:
			search = self.yandex(q, limit, count)
			search.run_crawl()
			emails.extend(search.emails)

		if "startpage" in engines:
			search = self.startpage(q, limit)
			search.run_crawl()
			emails.extend(search.emails)

		if "baidu" in engines:
			search = self.baidu(q, limit)
			search.run_crawl()
			emails.extend(search.emails)

		if "hunter" in engines:
			key = self.options["key"]
			search = self.hunter(q, key)
			search.run_crawl()
			emails.extend(search.emails)

		if "yippy" in engines:
			search = self.yippy(q)
			search.run_crawl()
			emails.extend(search.emails)

		emails = list(set(emails))
		for email in emails:
			self.output("\t%s" % email)

		self.save_gather({"emails" : emails}, "osint/email_search", name, output=self.options["output"])
