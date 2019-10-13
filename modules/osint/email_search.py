# -*- coding : utf-8 -*-

from core.module import BaseModule


class Module(BaseModule):

    meta = {
        "name": "Email Searcher",
        "author": "Saeed Dehqan(saeeddhqan)",
        "version": "0.1",
        "description": "Search in search engines for find emails. engines[bing,google,yahoo,yandex,beadu,ask]",
        "options": (
            ("company", BaseModule._global_options["target"], True, "Domain Name, Organization Name, etc"),
            ("limit", 3, True, "Search limit(min=1, max=15)"),
            ("count", 50, True, "Link count in page(min=10, max=100)"),
            ("engines", None, True, "Search engine names. e.g bing,google,..")
        )
    }

    def module_run(self):
        company = self.options["company"].replace("@", "")
        limit = self.options["limit"]
        count = self.options["count"]
        engines = self.options["engines"].split(",")
        run = self.search_eng("%40"+company, engines, limit, count)
        run.run_crawl()
        emails = self.page_parse(run.get_pages).get_emails(company)
        self.alert("Emails:")
        if(emails == []):
            self.output("\tWithout result")
        else:
            for i in emails:
                self.output("\t\"%s\"" % i)
