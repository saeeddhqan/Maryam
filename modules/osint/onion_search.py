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
