# -*- coding : utf-8 -*-

from core.module import BaseModule


class Module(BaseModule):

    meta = {
        "name": "Get Usernames in Social Networks",
        "author": "Saeed Dehqan(saeeddhqan)",
        "version": "0.1",
        "description": "Search for find Usernames in social networks. engines[bing,google,yahoo,yandex,metacrawler,ask]",
        "options": (
            ("company", BaseModule._global_options["target"], True, "Domain Name, Organization Name, etc"),
            ("engines", None, True, "Search engine names. e.g bing,google,.."),
            ("limit", 5, True, "Limit for search(min=1, max=15)"),
            ("count", 100, True, "Link count in page(min=10, max=100)")
        )
    }

    def module_run(self):
        company = self.options["company"]
        engines = self.options["engines"].split(",")
        limit = self.options["limit"]
        count = self.options["count"]
        run = self.search_eng(company, engines, limit, count)
        run.run_crawl()
        usernames = self.page_parse(run.get_pages).get_social_nets()
        self.alert("Social Networks:")
        for i in usernames:
            self.output("\t%s:" % i.title())
            if(usernames[i] != []):
                for j in usernames[i]:
                    self.output("\t\t\"%s\"" % j, "g")
            else:
                self.output("\t\tunknown")
