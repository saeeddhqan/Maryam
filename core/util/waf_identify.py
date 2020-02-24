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

from re import search, I


class waf_identify:
    """docstring for waf_identify"""

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
                             "framework", "get_waf", "run_crawl")
            if(con1 and con2 and con3):
                getattr(self, i)()

    def airlock(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"\AAL[_-]?(SESS|LB)=", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("Airlock (Phion/Ergon)")

    def anquanbao(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"x-powered-by-anquanbao", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("Anquanbao Web Application Firewall (Anquanbao)")

    def armor(self):
        mode = False
        mode |= search(
            r"This request has been blocked by website protection from Armor", self.content, I) is not None
        if(mode):
            self._waf.append("Armor Protection (Armor Defense)")

    def asm(self):
        mode = False
        mode |= search(
            r"The requested URL was rejected. Please consult with your administrator.", self.content, I) is not None
        if(mode):
            self._waf.append("Application Security Manager (F5 Networks)")

    def aws(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"\bAWS", header[1], I) is not None
        if(mode):

            self._waf.append(
                "Amazon Web Services Web Application Firewall (Amazon)")

    def baidu(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"fh1|yunjiasu-nginx", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("Yunjiasu Web Application Firewall (Baidu)")

    def barracuda(self):
        mode = False
        for header in self.headers.items():
            mode |= search(
                r"\Abarra_counter_session=|(\A|\b)barracuda_", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append(
                "Barracuda Web Application Firewall (Barracuda Networks)")

    def betterwpsecurity(self):
        mode = False
        mode |= search(
            r"/wp-self.content/plugins/better-wp-security/", self.content, I) is not None
        if(mode):
            self._waf.append("Better WP Security")

    def bigip(self):
        mode = False
        for header in self.headers.items():
            mode |= header[0].lower() == "x-cnection"
            mode |= header[0].lower() == "x-wa-info"
            mode |= search(
                r"\ATS\w{4,}=|bigip|bigipserver|\AF5\Z", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append(
                "BIG-IP Application Security Manager (F5 Networks)")

    def binarysec(self):
        mode = False
        for header in self.headers.items():
            mode |= header[0].lower() == "x-binarysec-via"
            mode |= header[0].lower() == "x-binarysec-nocache"
            mode |= search(r"binarySec", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("BinarySEC Web Application Firewall (BinarySEC)")

    def blockdos(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"blockdos\.net", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("BlockDos")

    def ciscoacexml(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"ace xml gateway", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("Cisco ACE XML Gateway (Cisco Systems)")

    def cloudflare(self):
        mode = False
        for header in self.headers.items():
            mode |= header[0].lower() == "cf-ray"
            mode |= search(
                r"__cfduid=|cloudflare-nginx|cloudflare[-]", header[1], I) is not None
            if(mode):
                break
        mode |= search(r"CloudFlare Ray ID:|var CloudFlare=",
                       self.content) is not None
        if(mode):
            self._waf.append(
                "CloudFlare Web Application Firewall (CloudFlare)")

    def cloudfront(self):
        mode = False
        for header in self.headers.items():
            mode |= header[0].lower() == "x-amz-cf-id"
            mode |= search(r"cloudfront", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("CloudFront (Amazon)")

    def comodo(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"protected by comodo waf",
                           header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("Comodo Web Application Firewall (Comodo)")

    def datapower(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"x-backside-transport", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("IBM WebSphere DataPower (IBM)")

    def denyall(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"sessioncookie=", header[1], I) is not None
            if(mode):
                break
        mode |= search(r"Condition Intercepted", self.content) is not None
        if(mode):
            self._waf.append("Deny All Web Application Firewall (DenyAll)")

    def dotdefender(self):
        mode = False
        for header in self.headers.items():
            mode |= header[0] == "x-dotdefender-denied"
            if(mode):
                break
        mode |= search(r"dotDefender Blocked Your Request",
                       self.content) is not None
        if(mode):
            self._waf.append("dotDefender (Applicure Technologies)")

    def edgecast(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"ecdf", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("EdgeCast WAF (Verizon)")

    def expressionengine(self):
        mode = False
        mode |= search(r"Invalid GET Data", self.content, I) is not None
        if(mode):
            self._waf.append("ExpressionEngine (EllisLab)")

    def fortiweb(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"fortiwafsid=", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("FortiWeb Web Application Firewall (Fortinet)")

    def hyperguard(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"odsession=", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append(
                "Hyperguard Web Application Firewall (art of defence)")

    def incapsula(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"incap_ses|visid_incap", header[1], I) is not None
            mode |= search(r"incapsula", header[1], I) is not None
            if(mode):
                break
        mode |= search(r"Incapsula incident ID", self.content) is not None
        if(mode):
            self._waf.append(
                "Incapsula Web Application Firewall (Incapsula/Imperva)")

    def isaserver(self):
        mode = False
        mode |= search(
            r"The server denied the specified Uniform Resource Locator (URL). Contact the server administrator.", self.content) is not None
        mode |= search(
            r"The ISA Server denied the specified Uniform Resource Locator (URL)", self.content) is not None
        if(mode):
            self._waf.append("ISA Server (Microsoft)")

    def jiasule(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"__jsluid=|jsl_tracking", header[1], I) is not None
            mode |= search(r"jiasule-waf", header[1], I) is not None
            if(mode):
                break
        mode |= search(
            r"static\.jiasule\.com/static/js/http_error\.js", self.content) is not None
        if(mode):
            self._waf.append("Jiasule Web Application Firewall (Jiasule)")

    def knownsec(self):
        mode = False
        mode |= search(r"url\('/ks-waf-error\.png'\)",
                       self.content) is not None
        if(mode):
            self._waf.append("KS-WAF (Knownsec)")

    def kona(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"AkamaiGHost", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("KONA Security Solutions (Akamai Technologies)")

    def modsecurity(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"Mod_Security|NOYB", header[1], I) is not None
            if(mode):
                break
        mode |= search(r"This error was generated by Mod_Security",
                       self.content) is not None
        if(mode):
            self._waf.append(
                "ModSecurity: Open Source Web Application Firewall (Trustwave)")

    def netcontinuum(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"NCI__SessionId=", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append(
                "NetContinuum Web Application Firewall (NetContinuum/Barracuda Networks)")

    def netscaler(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"(ns_af=|citrix_ns_id|NSC_)",
                           header[1], I) is not None
            mode |= search(r"ns.cache", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("NetScaler (Citrix Systems)")

    def newdefend(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"newdefend", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("Newdefend Web Application Firewall (Newdefend)")

    def nsfocus(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"nsfocus", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("NSFOCUS Web Application Firewall (NSFOCUS)")

    def paloalto(self):
        mode = False
        mode |= search(
            r"Access[^<]+has been blocked in accordance with company policy", self.content) is not None
        if(mode):
            self._waf.append("Palo Alto Firewall (Palo Alto Networks)")

    def profense(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"profense", header[1], I) is not None
            mode |= search(r"PLBSID=", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("Profense Web Application Firewall (Armorlogic)")

    def radware(self):
        mode = False
        for header in self.headers.items():
            mode |= header[0] == "x-sl-compstate"
            if(mode):
                break
        mode |= search(
            r"Unauthorized Activity Has Been Detected.+Case Number:", self.content) is not None
        if(mode):
            self._waf.append("AppWall (Radware)")

    def requestvalidationmode(self):
        mode = False
        mode |= search(
            r"ASP.NET has detected data in the request that is potentially dangerous", self.content) is not None
        mode |= search(
            r"Request Validation has detected a potentially dangerous client input value", self.content) is not None
        if(mode):
            self._waf.append("ASP.NET RequestValidationMode (Microsoft)")

    def safe3(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"Safe3 Web Firewall|Safe3",
                           header[1], I) is not None
            mode |= search(r"Safe3WAF", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("Safe3 Web Application Firewall")

    def safedog(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"safedog", header[1], I) is not None
            mode |= search(r"waf/2\.0", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("Safedog Web Application Firewall (Safedog)")

    def safedog(self):
        mode = False
        for header in self.headers.items():
            mode |= search(r"safedog", header[1], I) is not None
            mode |= search(r"waf/2\.0", header[1], I) is not None
            if(mode):
                break
        if(mode):
            self._waf.append("Safedog Web Application Firewall (Safedog)")

    def senginx(self):
        mode = False
        mode |= search(r"SENGINX-ROBOT-MITIGATION",
                       self.content, I) is not None
        if(mode):
            self._waf.append("SEnginx (Neusoft Corporation)")

    def sitelock(self):
        mode = False
        mode |= search(r"SiteLock Incident ID", self.content) is not None
        if(mode):
            self._waf.append("TrueShield Web Application Firewall (SiteLock)")

    def sonicwall(self):
        mode = False
        mode |= search(r"This request is blocked by the SonicWALL",
                       self.content) is not None
        mode |= search(r"Web Site Blocked.+\bnsa_banner",
                       self.content) is not None
        if("server" in self.headers):
            mode |= self.headers["server"] == "sonicwall"
        if(mode):
            self._waf.append("SonicWALL (Dell)")

    def sophos(self):
        mode = False
        mode |= search(r"Powered by UTM Web Protection",
                       self.content) is not None
        if(mode):
            self._waf.append("UTM Web Protection (Sophos)")

    def secureiis(self):
        mode = False
        mode |= search(
            r"SecureIIS[^<]+Web Server Protection", self.content) is not None
        mode |= search(r"http://www.eeye.com/SecureIIS/",
                       self.content) is not None
        mode |= search(
            r"\?subject=[^>]*SecureIIS Error", self.content) is not None
        if(mode):
            self._waf.append("SecureIIS Web Server Security (BeyondTrust)")

    def stingray(self):
        mode = False
        mode |= search(r"X-Mapping-", str(self.headers.keys()), I) is not None
        if(mode):
            self._waf.append(
                "Stingray Application Firewall (Riverbed / Brocade)")

    def sucuri(self):
        mode = False
        mode |= search(r"Questions\?.+cloudproxy@sucuri\.net",
                       self.content) is not None
        mode |= search(
            r"Sucuri WebSite Firewall - CloudProxy - Access Denied", self.content) is not None
        mode |= search(r"sucuri/cloudproxy",
                       str(self.headers.values()), I) is not None
        if(mode):
            self._waf.append("CloudProxy WebSite Firewall (Sucuri)")

    def teros(self):
        mode = False
        mode |= search(r"st8\(id|_wat|_wlf\)", str(
            self.headers.values()), I) is not None
        if(mode):
            self._waf.append(
                "Teros/Citrix Application Firewall Enterprise (Teros/Citrix Systems)")

    def trafficshield(self):
        mode = False
        if("server" in self.headers):
            mode |= self.headers["server"] == "F5-TrafficShield".lower()
        mode |= search(r"st8\(id|_wat|_wlf\)", str(
            self.headers.values()), I) is not None
        if(mode):
            self._waf.append("TrafficShield (F5 Networks)")

    def wallarm(self):
        mode = False
        if("server" in self.headers):
            mode |= self.headers["server"] == "nginx-wallarm"
        if(mode):
            self._waf.append("Wallarm Web Application Firewall (Wallarm)")

    def varnish(self):
        mode = False
        mode |= search(r"varnish|x-varnish",
                       str(self.headers.values()), I) is not None
        if(mode):
            self._waf.append("Varnish FireWall (OWASP)")

    def uspses(self):
        mode = False
        if("server" in self.headers):
            mode |= self.headers["server"] == "Secure Entry Server".lower()
        if(mode):
            self._waf.append(
                "USP Secure Entry Server (United Security Providers)")

    def urlscan(self):
        mode = False
        mode |= search("rejected-by-urlscan",
                       str(self.headers.values()), I) is not None
        mode |= search(r"Rejected-By-UrlScan", self.content, I) is not None
        if(mode):
            self._waf.append("UrlScan (Microsoft)")

    def webknight(self):
        mode = False
        if("server" in self.headers):
            mode |= self.headers["server"] == "WebKnight".lower()
        if(mode):
            self._waf.append("WebKnight Application Firewall (AQTRONIX)")

    def yundun(self):
        mode = False
        if("server" in self.headers):
            mode |= self.headers["server"] == "YUNDUN"
        if("x-cache" in self.headers.keys()):
            mode |= self.headers["x-cache"] == "YUNDUN"
        if(mode):
            self._waf.append("Yundun Web Application Firewall (Yundun)")

    def yunsuo(self):
        mode = False
        mode |= search(r"<img class=\"yunsuologo\"", self.content) is not None
        if "cookie" in self.headers.keys():
            mode |= search(r"yunsuo_session",
                           self.headers["cookie"], I) is not None
        if(mode):
            self._waf.append("Yunsuo Web Application Firewall (Yunsuo)")

    @property
    def get_waf(self):
        return self._waf
