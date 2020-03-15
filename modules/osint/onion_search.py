# -*- coding : u8 -*-

from core.module import BaseModule

class Module(BaseModule):

	meta = {
		"name": "Ahmia Onions Network Search",
		"author": "Saeeddqn",
		"version": "0.3",
		"description": "Ahmia's mission is to create the premier search engine for services residing on the Tor anonymity network.",
		"options": (
			("query", BaseModule._global_options["target"], True, "Domain Name, Company Name, keyword, etc", "-q", "store"),
			("output", False, False, "Save output to workspace", "--output", "store_true"),
		),
		"examples": ["onion_search -q <KEYWORD|COMPANY>", "onion_search -q <KEYWORD|COMPANY> --output"]
	}

	def module_run(self):
		q = self.options["query"]
		run = self.ahmia(q)
		run.run_crawl()
		links = run.links
		if links != []:
			for i in links:
				self.output("\t%s" % i, "g")
		else:
			self.output("Without Result")
		self.save_gather({"links" : links}, "osint/onion_search", q, output=self.options["output"])
