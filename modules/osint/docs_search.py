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
import re

class Module(BaseModule):

	meta = {
		"name": "Documentations Search",
		"author": "Saeeddqn",
		"version": "0.5",
		"description": "Search in engines for find related documents. filetypes[pdf,doc,docx,ppt,pptx,xlsx,txt, ..]",
		"options": (
			("query", BaseModule._global_options["target"], True, "Host Name, Company Name, , keyword, query, etc", "-q", "store"),
			("type", "pdf|doc", True, "File Type [pdf,doc,docx,ppt,pptx,xlsx,txt]. set with '|' separator", "-t", "store"),
			("limit", 2, False, "Limit for search(min=1)", "-l", "store"),
			("count", 50, False, "Links count in page(min=10)", "-c", "store"),
			("site", False, False, "If this is set, search just limited to the site", "-s", "store_false"),
			("engines", "google,bing", True, "Search Engines[bing,google,yahoo,yandex,metacrawler,ask,startpage,exalead,hunter] with comma separator", "-e", "store"),
			("key", None, False, "hunter.io api key", "-k", "store"),
			("output", False, False, "Save output to workspace", "--output", "store_false"),
		),
		"examples": ["docs_search -q amazon -t pdf -e google,bing,metacrawler", "docs_search -q amazon -t pdf -e google,bing,metacrawler -l 3"]
	}

	def module_run(self):
		q = self.options["query"]
		_type = self.options["type"].lower()
		limit = self.options["limit"]
		count = self.options["count"]
		engines = self.options["engines"].lower().split(",")
		fin = {}
		# Make dork
		if self.options["site"]:
			dork = self.urlib("\"%s\" filetype:%s site:%s" % (q, _type, self.options["site"])).quote
		else:
			dork = "%s filetype:%s" % (q, _type)
		reg = re.compile(r"<a href=\"[A-z0-9:/\.?\=_&;~\-+%s]+\.%s" %("%", _type))

		# Search to the engines
		if "google" in engines:
			search = self.google(dork, limit, count)
			search.run_crawl()
			fin["google"] = search.links

		if "bing" in engines:
			search = self.bing(dork, limit, count)
			search.run_crawl()
			fin["bing"] = search.docs

		if "yahoo" in engines:
			search = self.yahoo(dork, limit, count)
			search.run_crawl()
			fin["yahoo"] = search.docs

		if "metacrawler" in engines:
			search = self.metacrawler(dork, limit)
			search.run_crawl()
			fin["metacrawler"] = search.links

		if "yandex" in engines:
			search = self.yandex(dork, limit, count)
			search.run_crawl()
			fin["yandex"] = search.docs

		if "startpage" in engines:
			search = self.startpage(dork, limit)
			search.run_crawl()
			fin["startpage"] = search.docs

		if "baidu" in engines:
			search = self.baidu(dork, limit)
			search.run_crawl()
			fin["baidu"] = search.docs

		if "ask" in engines:
			search = self.ask(dork, limit)
			search.run_crawl()
			fin["ask"] = search.docs

		if "exalead" in engines:
			search = self.exalead(dork, limit)
			search.run_crawl()
			fin["exalead"] = search.docs

		if "hunter" in engines:
			search = self.hunter(dork, limit)
			search.run_crawl()
			fin["hunter"] = search.dns

		links = []
		self.alert("%s:" % _type.upper())
		for engine in fin:
			for link in fin[engine]:
				if link not in links:
					links.append(link)
				self.output("\t%s" % link, "g")
		self.save_gather({_type : links}, "osint/docs_search", q, [_type], output=self.options["output"])
