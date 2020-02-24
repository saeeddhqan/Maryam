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
