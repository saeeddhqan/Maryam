# -*- coding: u8 -*-
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

from re import search, I

class main:

	def __init__(self, framework, content, headers):
		self.framework = framework
		self.content = content
		self.headers = headers
		self._waf = []

	def run_crawl(self):
		for i in dir(self):
			con1 = not i.startswith("__")
			con2 = not i.endswith("__")
			con3 = i not in ("_waf", "content", "headers",
							 "framework", "waf", "run_crawl")
			if con1 and con2 and con3:
				getattr(self, i)()

	def airlock(self):
		M = False
		for header in self.headers.items():
			M |= search(r"\AAL[_-]?(SESS|LB)=", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("Airlock (Phion/Ergon)")

	def anquanbao(self):
		M = False
		for header in self.headers.items():
			M |= search(r"x-powered-by-anquanbao", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("Anquanbao Web Application Firewall (Anquanbao)")

	def armor(self):
		M = False
		M |= search(
			r"This request has been blocked by website protection from Armor", self.content, I) is not None
		if M:
			self._waf.append("Armor Protection (Armor Defense)")

	def asm(self):
		M = False
		M |= search(
			r"The requested URL was rejected. Please consult with your administrator.", self.content, I) is not None
		if M:
			self._waf.append("Application Security Manager (F5 Networks)")

	def aws(self):
		M = False
		for header in self.headers.items():
			M |= search(r"\bAWS", header[1], I) is not None
		if M:

			self._waf.append(
				"Amazon Web Services Web Application Firewall (Amazon)")

	def baidu(self):
		M = False
		for header in self.headers.items():
			M |= search(r"fh1|yunjiasu-nginx", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("Yunjiasu Web Application Firewall (Baidu)")

	def barracuda(self):
		M = False
		for header in self.headers.items():
			M |= search(
				r"\Abarra_counter_session=|(\A|\b)barracuda_", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append(
				"Barracuda Web Application Firewall (Barracuda Networks)")

	def betterwpsecurity(self):
		M = False
		M |= search(
			r"/wp-self.content/plugins/better-wp-security/", self.content, I) is not None
		if M:
			self._waf.append("Better WP Security")

	def bigip(self):
		M = False
		for header in self.headers.items():
			M |= header[0].lower() == "x-cnection"
			M |= header[0].lower() == "x-wa-info"
			M |= search(
				r"\ATS\w{4,}=|bigip|bigipserver|\AF5\Z", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append(
				"BIG-IP Application Security Manager (F5 Networks)")

	def binarysec(self):
		M = False
		for header in self.headers.items():
			M |= header[0].lower() == "x-binarysec-via"
			M |= header[0].lower() == "x-binarysec-nocache"
			M |= search(r"binarySec", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("BinarySEC Web Application Firewall (BinarySEC)")

	def blockdos(self):
		M = False
		for header in self.headers.items():
			M |= search(r"blockdos\.net", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("BlockDos")

	def ciscoacexml(self):
		M = False
		for header in self.headers.items():
			M |= search(r"ace xml gateway", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("Cisco ACE XML Gateway (Cisco Systems)")

	def cloudflare(self):
		M = False
		for header in self.headers.items():
			M |= header[0].lower() == "cf-ray"
			M |= search(
				r"__cfduid=|cloudflare-nginx|cloudflare[-]", header[1], I) is not None
			if M:
				break
		M |= search(r"CloudFlare Ray ID:|var CloudFlare=",
					   self.content) is not None
		if M:
			self._waf.append(
				"CloudFlare Web Application Firewall (CloudFlare)")

	def cloudfront(self):
		M = False
		for header in self.headers.items():
			M |= header[0].lower() == "x-amz-cf-id"
			M |= search(r"cloudfront", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("CloudFront (Amazon)")

	def comodo(self):
		M = False
		for header in self.headers.items():
			M |= search(r"protected by comodo waf",
						   header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("Comodo Web Application Firewall (Comodo)")

	def datapower(self):
		M = False
		for header in self.headers.items():
			M |= search(r"x-backside-transport", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("IBM WebSphere DataPower (IBM)")

	def denyall(self):
		M = False
		for header in self.headers.items():
			M |= search(r"sessioncookie=", header[1], I) is not None
			if M:
				break
		M |= search(r"Condition Intercepted", self.content) is not None
		if M:
			self._waf.append("Deny All Web Application Firewall (DenyAll)")

	def dotdefender(self):
		M = False
		for header in self.headers.items():
			M |= header[0] == "x-dotdefender-denied"
			if M:
				break
		M |= search(r"dotDefender Blocked Your Request",
					   self.content) is not None
		if M:
			self._waf.append("dotDefender (Applicure Technologies)")

	def edgecast(self):
		M = False
		for header in self.headers.items():
			M |= search(r"ecdf", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("EdgeCast WAF (Verizon)")

	def expressionengine(self):
		M = False
		M |= search(r"Invalid GET Data", self.content, I) is not None
		if M:
			self._waf.append("ExpressionEngine (EllisLab)")

	def fortiweb(self):
		M = False
		for header in self.headers.items():
			M |= search(r"fortiwafsid=", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("FortiWeb Web Application Firewall (Fortinet)")

	def hyperguard(self):
		M = False
		for header in self.headers.items():
			M |= search(r"odsession=", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append(
				"Hyperguard Web Application Firewall (art of defence)")

	def incapsula(self):
		M = False
		for header in self.headers.items():
			M |= search(r"incap_ses|visid_incap", header[1], I) is not None
			M |= search(r"incapsula", header[1], I) is not None
			if M:
				break
		M |= search(r"Incapsula incident ID", self.content) is not None
		if M:
			self._waf.append(
				"Incapsula Web Application Firewall (Incapsula/Imperva)")

	def isaserver(self):
		M = False
		M |= search(
			r"The server denied the specified Uniform Resource Locator (URL). Contact the server administrator.", self.content) is not None
		M |= search(
			r"The ISA Server denied the specified Uniform Resource Locator (URL)", self.content) is not None
		if M:
			self._waf.append("ISA Server (Microsoft)")

	def jiasule(self):
		M = False
		for header in self.headers.items():
			M |= search(r"__jsluid=|jsl_tracking", header[1], I) is not None
			M |= search(r"jiasule-waf", header[1], I) is not None
			if M:
				break
		M |= search(
			r"static\.jiasule\.com/static/js/http_error\.js", self.content) is not None
		if M:
			self._waf.append("Jiasule Web Application Firewall (Jiasule)")

	def knownsec(self):
		M = False
		M |= search(r"url\('/ks-waf-error\.png'\)",
					   self.content) is not None
		if M:
			self._waf.append("KS-WAF (Knownsec)")

	def kona(self):
		M = False
		for header in self.headers.items():
			M |= search(r"AkamaiGHost", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("KONA Security Solutions (Akamai Technologies)")

	def modsecurity(self):
		M = False
		for header in self.headers.items():
			M |= search(r"Mod_Security|NOYB", header[1], I) is not None
			if M:
				break
		M |= search(r"This error was generated by Mod_Security",
					   self.content) is not None
		if M:
			self._waf.append(
				"ModSecurity: Open Source Web Application Firewall (Trustwave)")

	def netcontinuum(self):
		M = False
		for header in self.headers.items():
			M |= search(r"NCI__SessionId=", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append(
				"NetContinuum Web Application Firewall (NetContinuum/Barracuda Networks)")

	def netscaler(self):
		M = False
		for header in self.headers.items():
			M |= search(r"(ns_af=|citrix_ns_id|NSC_)",
						   header[1], I) is not None
			M |= search(r"ns.cache", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("NetScaler (Citrix Systems)")

	def newdefend(self):
		M = False
		for header in self.headers.items():
			M |= search(r"newdefend", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("Newdefend Web Application Firewall (Newdefend)")

	def nsfocus(self):
		M = False
		for header in self.headers.items():
			M |= search(r"nsfocus", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("NSFOCUS Web Application Firewall (NSFOCUS)")

	def paloalto(self):
		M = False
		M |= search(
			r"Access[^<]+has been blocked in accordance with company policy", self.content) is not None
		if M:
			self._waf.append("Palo Alto Firewall (Palo Alto Networks)")

	def profense(self):
		M = False
		for header in self.headers.items():
			M |= search(r"profense", header[1], I) is not None
			M |= search(r"PLBSID=", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("Profense Web Application Firewall (Armorlogic)")

	def radware(self):
		M = False
		for header in self.headers.items():
			M |= header[0] == "x-sl-compstate"
			if M:
				break
		M |= search(
			r"Unauthorized Activity Has Been Detected.+Case Number:", self.content) is not None
		if M:
			self._waf.append("AppWall (Radware)")

	def requestvalidationM(self):
		M = False
		M |= search(
			r"ASP.NET has detected data in the request that is potentially dangerous", self.content) is not None
		M |= search(
			r"Request Validation has detected a potentially dangerous client input value", self.content) is not None
		if M:
			self._waf.append("ASP.NET RequestValidationM (Microsoft)")

	def safe3(self):
		M = False
		for header in self.headers.items():
			M |= search(r"Safe3 Web Firewall|Safe3",
						   header[1], I) is not None
			M |= search(r"Safe3WAF", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("Safe3 Web Application Firewall")

	def safedog(self):
		M = False
		for header in self.headers.items():
			M |= search(r"safedog", header[1], I) is not None
			M |= search(r"waf/2\.0", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("Safedog Web Application Firewall (Safedog)")

	def safedog(self):
		M = False
		for header in self.headers.items():
			M |= search(r"safedog", header[1], I) is not None
			M |= search(r"waf/2\.0", header[1], I) is not None
			if M:
				break
		if M:
			self._waf.append("Safedog Web Application Firewall (Safedog)")

	def senginx(self):
		M = False
		M |= search(r"SENGINX-ROBOT-MITIGATION",
					   self.content, I) is not None
		if M:
			self._waf.append("SEnginx (Neusoft Corporation)")

	def sitelock(self):
		M = False
		M |= search(r"SiteLock Incident ID", self.content) is not None
		if M:
			self._waf.append("TrueShield Web Application Firewall (SiteLock)")

	def sonicwall(self):
		M = False
		M |= search(r"This request is blocked by the SonicWALL",
					   self.content) is not None
		M |= search(r"Web Site Blocked.+\bnsa_banner",
					   self.content) is not None
		if "server" in self.headers:
			M |= self.headers["server"] == "sonicwall"
		if M:
			self._waf.append("SonicWALL (Dell)")

	def sophos(self):
		M = False
		M |= search(r"Powered by UTM Web Protection",
					   self.content) is not None
		if M:
			self._waf.append("UTM Web Protection (Sophos)")

	def secureiis(self):
		M = False
		M |= search(
			r"SecureIIS[^<]+Web Server Protection", self.content) is not None
		M |= search(r"http://www.eeye.com/SecureIIS/",
					   self.content) is not None
		M |= search(
			r"\?subject=[^>]*SecureIIS Error", self.content) is not None
		if M:
			self._waf.append("SecureIIS Web Server Security (BeyondTrust)")

	def stingray(self):
		M = False
		M |= search(r"X-Mapping-", str(self.headers.keys()), I) is not None
		if M:
			self._waf.append(
				"Stingray Application Firewall (Riverbed / Brocade)")

	def sucuri(self):
		M = False
		M |= search(r"Questions\?.+cloudproxy@sucuri\.net",
					   self.content) is not None
		M |= search(
			r"Sucuri WebSite Firewall - CloudProxy - Access Denied", self.content) is not None
		M |= search(r"sucuri/cloudproxy",
					   str(self.headers.values()), I) is not None
		if M:
			self._waf.append("CloudProxy WebSite Firewall (Sucuri)")

	def teros(self):
		M = False
		M |= search(r"st8\(id|_wat|_wlf\)", str(
			self.headers.values()), I) is not None
		if M:
			self._waf.append(
				"Teros/Citrix Application Firewall Enterprise (Teros/Citrix Systems)")

	def trafficshield(self):
		M = False
		if "server" in self.headers:
			M |= self.headers["server"] == "F5-TrafficShield".lower()
		M |= search(r"st8\(id|_wat|_wlf\)", str(
			self.headers.values()), I) is not None
		if M:
			self._waf.append("TrafficShield (F5 Networks)")

	def wallarm(self):
		M = False
		if "server" in self.headers:
			M |= self.headers["server"] == "nginx-wallarm"
		if M:
			self._waf.append("Wallarm Web Application Firewall (Wallarm)")

	def varnish(self):
		M = False
		M |= search(r"varnish|x-varnish",
					   str(self.headers.values()), I) is not None
		if M:
			self._waf.append("Varnish FireWall (OWASP)")

	def uspses(self):
		M = False
		if "server" in self.headers:
			M |= self.headers["server"] == "Secure Entry Server".lower()
		if M:
			self._waf.append(
				"USP Secure Entry Server (United Security Providers)")

	def urlscan(self):
		M = False
		M |= search("rejected-by-urlscan",
					   str(self.headers.values()), I) is not None
		M |= search(r"Rejected-By-UrlScan", self.content, I) is not None
		if M:
			self._waf.append("UrlScan (Microsoft)")

	def webknight(self):
		M = False
		if "server" in self.headers:
			M |= self.headers["server"] == "WebKnight".lower()
		if M:
			self._waf.append("WebKnight Application Firewall (AQTRONIX)")

	def yundun(self):
		M = False
		if "server" in self.headers:
			M |= self.headers["server"] == "YUNDUN"
		if "x-cache" in self.headers.keys():
			M |= self.headers["x-cache"] == "YUNDUN"
		if M:
			self._waf.append("Yundun Web Application Firewall (Yundun)")

	def yunsuo(self):
		M = False
		M |= search(r"<img class=\"yunsuologo\"", self.content) is not None
		if "cookie" in self.headers.keys():
			M |= search(r"yunsuo_session",
						   self.headers["cookie"], I) is not None
		if M:
			self._waf.append("Yunsuo Web Application Firewall (Yunsuo)")

	@property
	def waf(self):
		return self._waf
