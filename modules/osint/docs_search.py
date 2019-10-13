# -*- coding : utf-8 -*-

from core.module import BaseModule
import re

class Module(BaseModule):

    meta = {
        "name": "Document Search",
        "author": "Saeed Dehqan(saeeddhqan)",
        "version": "0.3",
        "description": "Search in google for find documents. filetypes[pdf,doc,docx,ppt,pptx,xlsx,txt]",
        "options": (
            ("company", BaseModule._global_options["target"], True, "Domain Name, Organization Name, etc"),
            ("type", None, True, "File Type [pdf,doc,docx,ppt,pptx,xlsx,txt]"),
            ("limit", 2, True, "Limit for search(min=1, max=10)"),
            ("count", 50, True, "Link count in page(min=10, max=100)"),
            ("metacrawler", False, True, "Search to metacrawler for more result")
        )
    }

    def module_run(self):
        company = self.options["company"]
        _type = self.options["type"]
        limit = self.options["limit"]
        count = self.options["count"]
        links = []
        if(_type.lower() not in ["pdf", "doc", "docx", "ppt", "pptx", "xlsx", "txt"]):
            self.error("File Type %s not found." % _type)
            return
        dork = self.urlib("ext:%s \"%s\"" % (_type, company)).quote()
        run = self.google_engine(dork, limit, count)
        run.run_crawl()
        pages = run.get_pages
        new_links = re.findall(r"<a href=\"[A-z0-9:/\.?\=_&;\-+%]+\.pdf", pages)
        for i in new_links:
            i = re.sub("<a href=\"", "", i)
            i = re.sub(r"$/url?q=", "", i) if re.search(r"$/url?q=", i) else i

        if(self.options["metacrawler"]):
            dork = "filetype:%s \"%s\"" % (_type, company)
            run = self.metacrawler_engine(dork)
            run.run_crawl()
            for x in run.get_links:
                links.append(x)

        self.alert("Result:")
        if(links != [] and links != None):
            for i in links:
                self.output("\t\"%s\"" % i, "g")
