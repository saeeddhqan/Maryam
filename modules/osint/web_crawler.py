#! /usr/bin/python
# -*- coding: u8 -*-
"""
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
