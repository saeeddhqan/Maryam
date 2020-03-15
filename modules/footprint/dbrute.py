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
import os

class Module(BaseModule):

	meta = {
		"name": "DNS/TLD Brute Force",
		"author": "Saeeddqn",
		"version": "0.2",
		"description": "Brute force DNS and DNS TLDs for find hostnames",
		"options": (
			("domain", BaseModule._global_options["target"],
			 True, "Domain name without https?://", "-d", "store"),
			("tld", False, False, "DNS TLD brute force mode", "--tld", "store_true"),
			("tldverbose", 349, False, "TLD brute force payloads len(min=1, max=count of payloads)", "--tldverbose", "store"),
			("dnsverbose", 790, False, "DNS brute force payloads len(min=1, max=count of payloads)", "--dnsverbose", "store"),
			("dnslist", os.path.join(BaseModule.data_path, 'dnsnames.txt'), False, "DNS wordlist(with \\n separator).Default dnsnames.txt on data", "--dnslist", "store"),
			("tldlist", os.path.join(BaseModule.data_path, 'tlds.txt'), False, "TLD wordlist(with \\n separator).Default tlds.txt on data", "--tldlist", "store"),
			("output", False, False, "Save output to the workspace", "--output", "store_true"),
		),
		"examples": ["dbrute -d <DOMAIN> --tld --tldverbose 50 --output", "dbrute -d <DOMAIN> --dnslist <WORDLIST>"]
	}

	def module_run(self):
		host = self.options["domain"]
		host_attr = self.urlib(host)
		host = host_attr.sub_service("https")
		hostname = self.urlib(host).netloc
		resp = {}
		out = self.options["output"]
		methods = []

		### TLD Brute Force ####
		########################
		if self.options["tld"]:
			# Full version of http://data.iana.org/TLD/tlds-alpha-by-domain.txt
			tld_list = self.options["tldlist"]
			# # Read file and split it and setting verbose
			try:
				with open(tld_list) as tlist:
					tlist = tlist.read().split()
					tlen = len(tlist)
			except Exception as e:
				raise e

			verb = self.options["tldverbose"]
			verb = tlen if verb > tlen else verb
			hostname = host.split('.')[0]
			tld = []
			self.heading("Start DNS/TLD brute force with %d payload" % verb, level=0)
			for i in range(0, len(tlist[:verb])):
				tmp_hname = "%s.%s" % (hostname, tlist[i])
				try:
					req = self.request(tmp_hname)
				except Exception:
					pass
				else:
					self.output("\t%s" % tmp_hname, "g")
					if out:
						tld.append(tmp_hname)

			if out:
				resp["tld"] = tld
				methods.append("tld")

		### DNS Brute Force ####
		########################

		max_attempt = 4
		attempt = 0
		# Read file and split it and setting verbose
		dns_list = self.options["dnslist"]
		dns = []
		try:
			with open(dns_list) as dlist:
				dlist = dlist.read().split()
				dlen = len(dlist)
				verb = self.options["dnsverbose"]
				verb = dlen if verb > dlen else verb
		except Exception as e:
			raise e

		self.heading("Start DNS brute force with %d payload" % verb, level=0)
		for i in dlist[:verb]:
			if attempt > max_attempt:
				break
			tmp_name = "https://%s.%s" % (i, hostname)
			try:
				req = self.request(tmp_name)
			except Exception as e:
				if "timed out" in str(e.args):
					self.verbose("%s => Timed out" % tmp_name, "O")
					attempt += 1
				else:
					self.verbose("%s:\"%s\"" % (list(e.args)[0], tmp_name), "O")
			else:
				dns.append(tmp_name)
				self.output("\"%s\"" % tmp_name, "G")
		if dns == []:
			self.output("\tWithout hit")
		resp["dnsbrute"] = dns
		methods.append("dnsbrute")

		self.save_gather(resp, "footprint/dbrute", host, methods, output=out)
