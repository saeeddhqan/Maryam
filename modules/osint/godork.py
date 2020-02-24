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
