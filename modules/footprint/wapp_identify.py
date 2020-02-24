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
        "name": "Web Application Identify",
        "author": "Saeed Dehqan(saeeddhqan)",
        "version": "0.1",
        "description": "Web fingerprinting to identify programs used with over 100 pyload.",
        "options": (
            ("url", BaseModule._global_options["target"], True, "URL string"),
            ("cms", True, True, "Use CMS identify"),
            ("frameworks", True, True, "Use Frameworks identify"),
            ("os", True, True, "Use OS identify"),
            ("lang", True, True, "Use Language identify"),
            ("waf", True, True, "use WAF identify")
        )
    }

    def module_run(self):
        url = self.options["url"]
        request = self.request(url)

        if(self.options["os"]):
            _os = self.os_identify(request.text, request.headers)
            _os.run_crawl()
            os = _os.get_os if _os.get_os != None else "unknow"
            self.alert("OS Server : \"%s\"" % os)

        if(self.options["cms"]):
            _cms = self.cms_identify(request.text, request.headers)
            _cms.run_crawl()
            cms = _cms.get_cms if _cms.get_cms != None else "unknow"
            self.alert("Web CMS : \"%s\"" % cms)

        if(self.options["lang"]):
            _lang = self.lang_identify(request.text, request.headers)
            _lang.run_crawl()
            lang = _lang.get_lang if _lang.get_lang != None else "unknow"
            self.alert("Web Language : \"%s\"" % lang)

        if(self.options["frameworks"]):
            _frameworks = self.frameworks_identify(
                request.text, request.headers)
            _frameworks.run_crawl()
            frameworks = _frameworks.get_frameworks
            for i in frameworks:
                self.output("Use \"%s\"" % (i))

        if(self.options["waf"]):
            _waf = self.waf_identify(request.text, request.headers)
            _waf.run_crawl()
            waf = _waf.get_waf
            if(waf == []):
                self.alert("WAF : not found")
            else:
                self.alert("WAF : ")
                for i in waf:
                    self.output("\t\"%s\"" % i, "g")
