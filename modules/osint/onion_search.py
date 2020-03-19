# -*- coding : u8 -*-

from core.module import BaseModule

class Module(BaseModule):

	meta = {
		"name": "Onions Network Search",
		"author": "Saeeddqn",
		"version": "0.4",
		"description": "onion_search is to create the premier search engine for services residing on the Tor anonymity network.",
		"sources": ("ahmia","onionland"),
		"options": (
			("query", BaseModule._global_options["target"], True, "Domain Name, Company Name, keyword, etc", "-q", "store"),
			("output", False, False, "Save output to workspace", "--output", "store_true"),
		),
		"examples": ("onion_search -q <KEYWORD|COMPANY>", "onion_search -q <KEYWORD|COMPANY> --output")
	}

	def module_run(self):
		q = self.options["query"]
		ahmia = self.ahmia(q)
		ahmia.run_crawl()
		links = ahmia.links
		onionland = self.onionland(q, limit=5)
		onionland.run_crawl()
		links.extend(onionland.links)


		links = links(set(links))
		if links != []:
			for i in links:
				self.output("\t%s" % i, "g")
		else:
			self.output("Without Result")
			return
		self.save_gather({"links" : links}, "osint/onion_search", q, output=self.options["output"])
