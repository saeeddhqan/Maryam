# -*- coding : utf-8 -*-

from core.module import BaseModule


class Module(BaseModule):

    meta = {
        "name": "Google Dork Search",
        "author": "Saeed Dehqan(saeeddhqan)",
        "version": "0.1",
        "description": "Search your dork in google and get response",
        "options": (
            ("dork", None, True, "Google dork string"),
            ("limit", 2, True, "Google search limit(min=1, max=15)"),
            ("count", 50, True, "Link count in page(min=10, max=100)")
        )
    }

    def module_run(self):
        dork = self.options["dork"]
        limit = self.options["limit"]
        count = self.options["count"]
        run = self.google_engine(dork, limit, count)
        run.run_crawl()
        urls = self.page_parse(run.get_pages).get_sites()

        self.alert("urls:")
        if(urls != []):
            for i in urls:
                self.output("\t\"%s\"" % i, "g")
        else:
            self.output("Without result")
