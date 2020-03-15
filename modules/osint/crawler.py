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
from lxml.html import fromstring

class Module(BaseModule):

	meta = {
		"name": "Web Crawler",
		"author": "Saeeddqn",
		"version": "0.4",
		"description": "Crawl web pages for find links, JS Files, CSS files, Comments And everything else interesting",
		"options": (
			("domain", BaseModule._global_options["target"], True, "Domain string", "-d", "store"),
			("crawl", False, False, "Crawl in the more pages", "--crawl", "store_true"),
			("debug", False, False, "debug the scraper", "--debug", "store_true"),
			("limit", 20, False, "The number of pages that open", "-l", "store"),
			("output", False, False, "Save output to workspace", "--output", "store_true"),
		),
		"examples": ["crawler -d <DOMAIN> --output --debug -l 10", "crawler -d <DOMAIN> --crawl --output"]
	}

	def module_run(self):
		domain = self.options["domain"]
		run = self.web_scrap(domain, self.options["crawl"], self.options["debug"], self.options["limit"])
		run.run_crawl()
		e = {"js": run.js, "cdn": run.cdn,
			 "query": run.query_links, "exlinks": run.external_links, 
			 "links": run.links, "css": run.css, "comments": run.comments, 
			 "emails" : run.emails, "phones" : run.phones}

		for i in e:
			self.alert(i)
			if e[i] == []:
				self.output("\t..")
			else:
				for j in e[i]:
					self.output("\t\"%s\"" % j, "o")

		for i in run.social_nets:
			self.alert(i)
			if run.social_nets[i] != []:
				for j in run.social_nets[i]:
					self.output("\t\t%s" % str(j), "g")
			else:
				self.output("\t\t-")

		e["Social Networks"] = run.social_nets

		self.save_gather(e, "osint/crawler", domain, output=self.options["output"])
