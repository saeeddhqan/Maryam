# -*- coding : utf-8 -*-

from core.module import BaseModule


class Module(BaseModule):

    meta = {
        "name": "Web Crawler",
        "author": "Saeed Dehqan(saeeddhqan)",
        "version": "0.2",
        "description": "Extract js,css files,comments,links from web page",
        "options": (
            ("url", None, True, "url for crawl"),
        )
    }

    def module_run(self):
        url = self.options["url"]
        run = self.web_scrap(url)
        run.run_crawl()
        e = {"JS links": run.get_js, "CDN(Content Delivery Network) links": run.get_cdn,
             "Query Links": run.get_query_links, "External links": run.get_external_links, "Links": run.get_links, "CSS Files" : run.get_css, "Comments" : run.get_comments}

        for i in e:
            self.alert(i)
            if(e[i] == []):
                self.output("\t..")
            else:
                for j in e[i]:
                    self.output("\t\"%s\"" % j, "o")
