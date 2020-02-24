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
