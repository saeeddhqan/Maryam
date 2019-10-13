# -*- coding : utf-8 -*-

from core.module import BaseModule

class Module(BaseModule):

    meta = {
        "name": "Ahmia Tor Search",
        "author": "Saeed Dehqan(saeeddhqan)",
        "version": "0.1",
        "description": "Ahmia's mission is to create the premier search engine for services residing on the Tor anonymity network.",
        "options": (
            ("company", BaseModule._global_options["target"], True, "Domain Name, Organization Name, etc"),
        )
    }

    def module_run(self):
        company = self.options["company"]
        run = self.ahmia_engine(company)
        run.run_crawl()
        links = run.get_links
        if(links != []):
            for i in links:
                self.output("\t\"%s\"" % i, "g")
        else:
            self.output("Without Result")
