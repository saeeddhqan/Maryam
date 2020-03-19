# -*- coding : u8 -*-
"""
OWASP Maryam!

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
		"name": "Web Applications Identifier",
		"author": "Saeeddqn",
		"version": "0.2",
		"description": "Web fingerprinting to identify the applications used with over 500 pyload.",
		"options": (
			("domain", BaseModule._global_options["target"], True, "Domain string", "-d", "store"),
			("output", False, False, "Save output to workspace", "--output", "store_true"),
		),
		"examples": ["wapps -d <DOMAIN>"]
	}

	def module_run(self):
		domain = self.options["domain"]
		req = self.request(domain)
		headers = req.headers
		text = req.text
		resp = {}
		v = self.wapps(domain, text, headers)
		wapps = v.run_crawl()
		self.alert("WAPPS:")
		resp["wapps"] = []
		for i in wapps:
			self.output("\t%s : %s"%(i,wapps[i]), "g")
			resp["wapps"].append((i,wapps[i]))

		_os = self.os_identify(text, headers)
		_os.run_crawl()
		_os = _os.os if _os.os != None else "unknow"
		resp["os"] = _os
		self.alert("Used \"%s\" operating system" % _os)

		_cms = self.cms_identify(text, headers)
		_cms.run_crawl()
		cms = _cms.cms if _cms.cms != None else "unknow"
		resp["cms"] = cms
		self.alert("Web CMS is \"%s\"" % cms)

		_lang = self.lang_identify(text, headers)
		_lang.run_crawl()
		lang = _lang.lang if _lang.lang != None else "unknow"
		resp["lang"] = lang
		self.alert("Web Language is \"%s\"" % lang)
	  
		resp["frameworks"] = []
		_frameworks = self.frameworks_identify(text, headers)
		_frameworks.run_crawl()
		frameworks = _frameworks.frameworks
		for i in frameworks:
			self.output("Use \"%s\"" % (i))
			resp["frameworks"].append(i)

		resp["waf"] = []
		_waf = self.waf_identify(text, headers)
		_waf.run_crawl()
		waf = _waf.waf
		if waf != []:
			self.alert("WAF: ")
			for i in waf:
				resp["waf"].append(i)
				self.output("\t\"%s\"" % i, "g")
					
		self.save_gather(resp, "footprint/wapps", domain, output=self.options["output"])
