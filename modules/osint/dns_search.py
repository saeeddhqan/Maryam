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
import re
import os


class Module(BaseModule):

	meta = {
		"name": "DNS Searcher",
		"author": "Saeeddqn",
		"version": "1.5",
		"description": "Search in the search engines and other sources for find DNS. engines[bing,google,yahoo,yandex,metacrawler,ask,\
						baidu,startpage,netcraft,threatcrowd,virustotal,yippy]",
		"sources": ("bing", "google", "yahoo", "yandex", "metacrawler", "ask", "baidu", "startpage",
					"netcraft", "threatcrowd", "virustotal", "yippy", "otx"),
		"options": (
			("domain", BaseModule._global_options["target"],
			 True, "Domain name without https?://", "-d", "store"),
			("limit", 3, False, "Search limit", "-l", "store"),
			("count", 50, False, "Links count in page(min=10, max=100)", "-c", "store"),
			("engines", None, True, "Search engine names. e.g bing,google,..", "-e", "store"),
			("output", False, False, "Save output to workspace", "--output", "store_true"),
		),
		"examples": ("dns_search -d example.com --output -e google,bing,yahoo -l 3", "dns_search -d example.com --dumpster --output")

	}

	def module_run(self):
		domain = self.options["domain"]
		domain_attr = self.urlib(domain)
		domain = domain_attr.sub_service("http")
		domain_name = self.urlib(domain).netloc
		domain_names = []
		fin = {}
		limit = self.options["limit"]
		count = self.options["count"]
		engines = self.options["engines"].lower().split(",")

		if "threatcrowd" in engines:
			self.alert("ThreatCrowd")
			req = self.request(
				"https://threatcrowd.org/searchApi/v2/domain/report/?domain=" + domain_name)
			txt = re.sub("[\t\n ]+", "", req.text)
			txt = re.findall(
				r"\"subdomains\":(\[[\"\.A-z0-9_\-,]+\])", txt)
			hosts = list(set(txt[0][1:-1].split(",")))
			for host in hosts:
				host = host[1:-1]
				domain_names.append(host)
				self.output("\t%s"%host)

		if "virustotal" in engines:
			self.alert("VirusTotal")
			req = self.request("https://www.virustotal.com/ui/domains/%s/subdomains?relationships=resolutions&cursor=STMwCi4=&limit=40" % domain_name)
			parser = self.page_parse(req.text).get_dns(domain_name)
			for host in list(set(parser)):
				if host[0].isdigit():
					matches = re.match(r'.+([0-9])[^0-9]*$', host)
					host = host[matches.start(1) + 1:]
				domain_names.append(host)
				self.output("\t%s"%host)

		if "otx" in engines:
			self.alert("otx")
			req = self.request("https://otx.alienvault.com/api/v1/indicators/domain/%s/passive_dns" % domain_name)
			parser = self.page_parse(req.text).get_dns(domain_name)
			for host in list(set(parser)):
				domain_names.append(host)
				self.output("\t%s"%host)

		if "google" in engines:
			search = self.google(domain_name, limit, count)
			search.run_crawl()
			fin["google"] = search.dns

		if "bing" in engines:
			search = self.bing(domain_name, limit, count)
			search.run_crawl()
			fin["bing"] = search.dns

		if "yahoo" in engines:
			search = self.yahoo(domain_name, limit, count)
			search.run_crawl()
			fin["yahoo"] = search.dns

		if "metacrawler" in engines:
			search = self.metacrawler(domain_name, limit)
			search.run_crawl()
			fin["metacrawler"] = search.dns

		if "yandex" in engines:
			search = self.yandex(domain_name, limit, count)
			search.run_crawl()
			fin["yandex"] = search.dns

		if "startpage" in engines:
			search = self.startpage(domain_name, limit)
			search.run_crawl()
			fin["startpage"] = search.dns

		if "baidu" in engines:
			search = self.baidu(domain_name, limit)
			search.run_crawl()
			fin["baidu"] = search.dns

		if "netcraft" in engines:
			search = self.netcraft(domain_name)
			search.run_crawl()
			fin["netcraft"] = search.dns

		if "yippy" in engines:
			search = self.yippy(domain_name)
			search.run_crawl()
			fin["yippy"] = search.dns
			
		for eng in fin:
			self.alert(eng)
			for host in list(set(fin[eng])):
				if "%" not in host:
					domain_names.append(host)
					self.output("\t%s"%host)

		self.save_gather(domain_names, "osint/dns_search", domain_name, output=self.options["output"])
