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
# Sources: https://github.com/EnableSecurity/wafw00f and ....

from re import search, I

class main:

	def __init__(self, req):
		""" detect WAFs(Web Application Firewalls)
			
			req		  : Request attribute
		"""
		self.req = req
		self.content = req.text
		self.headers = req.headers
		self.status_code = req.status_code
		self.reason = req.reason
		self._waf = []

	def run_crawl(self):
		for attr in dir(self):
			con1 = not attr.startswith('__')
			con2 = not attr.endswith('__')
			con3 = attr not in ('_waf', 'content', 'headers',
							 'waf', 'run_crawl', 'status_code', 'reason',
							 'header_check', 'status_check', 'reason_check', 'content_check',
							 'cookie_check', 'req', 'framework')
			if con1 and con2 and con3:
				getattr(self, attr)()

	def header_check(self, tup):
		header, match = tup
		value = self.headers.get(header)
		if value:
			# set-cookie can have multiple headers, python gives it to us
			# concatinated with a comma
			if header == 'Set-Cookie':
				values = value.split(', ')
			else:
				values = [value]
			for value in values:
				if search(match, value, I):
					return True
		return False

	def status_check(self, code):
		if self.status_code == code:
			return True
		return False

	def cookie_check(self, match, attack=False):
		return self.header_check(('Set-Cookie', match))

	def reason_check(self, reason_code):
		if str(self.reason) == reason_code:
			return True
		return False

	def content_check(self, regex):
		if search(regex, self.content, I):
			return True
		return False

	def AzionCDN(self):
		s = [
			self.header_check(('Server', r'Azion([-_]CDN)?'))
		]
		if any(s):
			self._waf.append('AzionCDN (AzionCDN)')

	def WatchGuard(self):
		s = [
			self.header_check(('Server', 'WatchGuard')),
			self.content_check(r"Request denied by WatchGuard Firewall"),
			self.content_check(r'WatchGuard Technologies Inc\.')
		]
		if any(s):
			self._waf.append('WatchGuard (WatchGuard Technologies)')

	def iFinity_DotNetNuke(self):
		schema1 = [
			self.header_check(('X-UrlMaster-Debug', '.+')),
			self.header_check(('X-UrlMaster-Ex', '.+')),
		]
		schema2 = [
			self.content_check(r"Ur[li]RewriteModule"),
			self.content_check(r'SecurityCheck')
		]
		if any(i for i in schema1):
			self._waf.append('URLMaster SecurityCheck (iFinity/DotNetNuke)')
		if all(i for i in schema2):
			self._waf.append('URLMaster SecurityCheck (iFinity/DotNetNuke)')

	def PT_Application_Firewall(self):
		s = [
			self.content_check(r'<h1.{0,10}?Forbidden'),
			self.content_check(r'<pre>Request.ID:.{0,10}?\d{4}\-(\d{2})+.{0,35}?pre>')
		]
		if all(i for i in s):
			self._waf.append('PT Application Firewall (Positive Technologies)')
	

	def Indusface(self):
		s = [
			self.header_check(('Server', r'IF_WAF')),
			self.content_check(r'This website is secured against online attacks. Your request was blocked')
		]
		if any(s):
			self._waf.append('IndusGuard (Indusface)')

	def Armor(self):
		s = [
			self.content_check(r'blocked by website protection from armor'),
			self.content_check(r'please create an armor support ticket')
		]
		if any(s):
			self._waf.append('Armor Defense (Armor)')

	def SquidProxy(self):
		s = [
			self.header_check(('Server', r'squid(/[0-9\.]+)?')),
			self.content_check(r'Access control configuration prevents your request')
			]
		if all(i for i in s):
			self._waf.append('SquidProxy IDS (SquidProxy)')

	def ASPA_Firewall(self):
		s = [
			self.header_check(('Server', r'ASPA[\-_]?WAF')),
			self.header_check(('ASPA-Cache-Status', r'.+?'))
		]
		if any(s):
			self._waf.append('ASPA Firewall (ASPA Engineering Co.)')

	def AQTRONIX(self):
		schema1 = [
			self.status_check(999),
			self.reason_check('No Hacking')
		]    
		schema2 = [
			self.status_check(404),
			self.reason_check('Hack Not Found')
		]
		schema3 = [
			self.content_check(r'WebKnight Application Firewall Alert'),
			self.content_check(r'What is webknight\?'),
			self.content_check(r'AQTRONIX WebKnight is an application firewall'),
			self.content_check(r'WebKnight will take over and protect'),
			self.content_check(r'aqtronix\.com/WebKnight'),
			self.content_check(r'AQTRONIX.{0,10}?WebKnight'),
		]
		if all(i for i in schema1):
			self._waf.append('WebKnight (AQTRONIX)')
		if all(i for i in schema2):
			self._waf.append('WebKnight (AQTRONIX)')    
		if any(i for i in schema3):
			self._waf.append('WebKnight (AQTRONIX)')

	def SecureSphere(self):
		s = [
			self.content_check(r'<(title|h2)>Error'),
			self.content_check(r'The incident ID is'),
			self.content_check(r"This page can't be displayed"),
			self.content_check(r'Contact support for additional information')
		]
		if all(i for i in s):
			self._waf.append('SecureSphere (Imperva Inc.)')

	def WP_Cerber_Security(self):
		s = [
			self.content_check(r'your request looks suspicious or similar to automated'),
			self.content_check(r'our server stopped processing your request'),
			self.content_check(r'We.re sorry.{0,10}?you are not allowed to proceed'),
			self.content_check(r'requests from spam posting software'),
			self.content_check(r'<title>403 Access Forbidden')
			]
		if all(i for i in s):
			self._waf.append('WP Cerber Security (Cerber Tech)')

	def Cloudrity(self):
		s = [
			self.content_check(r"Access Denied.{0,10}?Viettel WAF"),
			self.content_check(r"cloudrity\.com\.(vn)?/"),
			self.content_check(r"Viettel WAF System")
		]
		if any(s):
			self._waf.append('Viettel (Cloudrity)')

	def Cloudfloor(self):
		s = [
			self.header_check(('Server', r'CloudfloorDNS(.WAF)?')),
			self.content_check(r'<(title|h\d{1})>CloudfloorDNS.{0,6}?Web Application Firewall Error'),
			self.content_check(r'www\.cloudfloordns\.com/contact')
		]
		if any(s):
			self._waf.append('Cloudfloor (Cloudfloor DNS)')

	def NAXSI(self):
		s = [
			self.header_check(('X-Data-Origin', r'^naxsi(.+)?')),
			self.header_check(('Server', r'naxsi(.+)?')),
			self.content_check(r'blocked by naxsi'),
			self.content_check(r'naxsi blocked information')
		]
		if any(s):
			self._waf.append('NAXSI (NBS Systems)')

	def Distil(self):
		s = [
			self.content_check(r'cdn\.distilnetworks\.com/images/anomaly\.detected\.png'),
			self.content_check(r'distilCaptchaForm'),
			self.content_check(r'distilCallbackGuard')
		]
		if any(s):
			self._waf.append('Distil (Distil Networks)')

	def Edgecast(self):
		s = [
			self.header_check(('Server', r'^ECD(.+)?')),
			self.header_check(('Server', r'^ECS(.*)?'))
		]
		if any(s):
			self._waf.append('Edgecast (Verizon Digital Media)')

	def WebTotem(self):
		s = [
			self.content_check(r"The current request was blocked.{0,8}?>WebTotem")
		]
		if any(s):
			self._waf.append('WebTotem (WebTotem)')

	def Fortinet(self):
		schema1 = [
			self.cookie_check(r'^FORTIWAFSID='),
			self.content_check('.fgd_icon')
		]
		schema2 = [
			self.content_check('fgd_icon'),
			self.content_check('web.page.blocked'),
			self.content_check('url'),
			self.content_check('attack.id'),
			self.content_check('message.id'),
			self.content_check('client.ip')
		]
		if any(i for i in schema1):
			self._waf.append('FortiWeb (Fortinet)')
		if all(i for i in schema2):
			self._waf.append('FortiWeb (Fortinet)')

	def NexusGuard(self):
		s = [
			self.content_check(r'Powered by Nexusguard'),
			self.content_check(r'nexusguard\.com/wafpage/.+#\d{3};')
		]
		if any(s):
			self._waf.append('NexusGuard Firewall (NexusGuard)')

	def Yunsuo(self):
		s = [
			self.cookie_check(r'^yunsuo_session='),
			self.content_check(r'class=\"yunsuologo\"')
		]
		if any(s):
			self._waf.append('Yunsuo (Yunsuo)')

	def PentaWAF(self):
		s = [
			self.header_check(('Server', r'PentaWaf(/[0-9\.]+)?')),
			self.content_check(r'Penta.?Waf/[0-9\.]+?.server')
		]
		if any(s):
			self._waf.append('PentaWAF (Global Network Services)')

	def Anquanbao(self):
		s = [
			self.header_check(('X-Powered-By-Anquanbao', '.+?')),
			self.content_check(r'aqb_cc/error/')
			]
		if any(s):
			self._waf.append('Anquanbao (Anquanbao)')

	def Xuanwudun(self):
		s = [
			self.content_check(r"admin\.dbappwaf\.cn/(index\.php/Admin/ClientMisinform/)?"),
			self.content_check(r'class=.(db[\-_]?)?waf(.)?([\-_]?row)?>')
		]
		if any(s):
			self._waf.append('Xuanwudun (Xuanwudun)')

	def Neusoft(self):
		s = [
			self.content_check(r'SENGINX\-ROBOT\-MITIGATION')
		]
		if any(s):
			self._waf.append('SEnginx (Neusoft)')

	def WebLand(self):
		s = [
			self.header_check(('Server', r'protected by webland'))
		]
		if any(s):
			self._waf.append('WebLand (WebLand)')

	def aeSecure(self):
		s = [
			self.header_check(('aeSecure-code', '.+?')),
			self.content_check(r'aesecure_denied\.png')
		]
		if any(s):
			self._waf.append('aeSecure (aeSecure)')

	def Tencent_Cloud_Firewall(self):
		s = [
			self.content_check(r'waf\.tencent\-?cloud\.com/')
		]
		if any(s):
			self._waf.append('Tencent Cloud Firewall (Tencent Technologies)')

	def VirusDie(self):
		s = [
			self.content_check(r"cdn\.virusdie\.ru/splash/firewallstop\.png"),
			self.content_check(r'copy.{0,10}?Virusdie\.ru')
		]
		if any(s):
			self._waf.append('VirusDie (VirusDie LLC)')

	def YXLink(self):
		s = [
			self.cookie_check(r'^yx_ci_session='),
			self.cookie_check(r'^yx_language='),
			self.header_check(('Server', r'Yxlink([\-_]?WAF)?'))
		]
		if any(s):
			self._waf.append('YXLink (YxLink Technologies)')

	def Amazon(self):
		s = [
			# This is standard detection schema, checking the server header
			self.header_check(('Server', 'Cloudfront')),
			# Found samples returning 'Via: 1.1 58bfg7h6fg76h8fg7jhdf2.cloudfront.net (CloudFront)'
			self.header_check(('Via', r'([0-9\.]+?)? \w+?\.cloudfront\.net \(Cloudfront\)')),
			# The request token is sent along with this header, eg:
			# X-Amz-Cf-Id: sX5QSkbAzSwd-xx3RbJmxYHL3iVNNyXa1UIebDNCshQbHxCjVcWDww==
			self.header_check(('X-Amz-Cf-Id', '.+?')),
			# This is another reliable fingerprint found on headers
			self.header_check(('X-Cache', 'Error from Cloudfront')),
			# These fingerprints are found on the blockpage itself
			self.content_check(r'Generated by cloudfront \(CloudFront\)')
		]
		if any(s):
			self._waf.append('Cloudfront (Amazon)')

	def SpiderLabs(self):
		schema1 = [
			self.header_check(('Server', r'(mod_security|Mod_Security|NOYB)')),
			self.content_check(r'This error was generated by Mod.?Security'),
			self.content_check(r'rules of the mod.security.module'),
			self.content_check(r'mod.security.rules triggered'),
			self.content_check(r'Protected by Mod.?Security'),
			self.content_check(r'/modsecurity[\-_]errorpage/'),
			self.content_check(r'modsecurity iis')
		]
		schema2 = [
			self.reason_check('ModSecurity Action'),
			self.status_check(403)
		]
		schema3 = [
			self.reason_check('ModSecurity Action'),
			self.status_check(406)
		]
		if any(i for i in schema1):
			self._waf.append('ModSecurity (SpiderLabs)')
		if all(i for i in schema2):
			self._waf.append('ModSecurity (SpiderLabs)')
		if all(i for i in schema3):
			self._waf.append('ModSecurity (SpiderLabs)')

	def Amazon(self):
		s = [
			self.header_check(('X-AMZ-ID', '.+?')),
			self.header_check(('X-AMZ-Request-ID', '.+?')),
			self.cookie_check(r'^aws.?alb='),
			self.header_check(('Server', r'aws.?elb'))
		]
		if any(s):
			self._waf.append('AWS Elastic Load Balancer (Amazon)')

	def ChinaCache(self):
		s = [
			self.header_check(('Powered-By-ChinaCache', '.+'))
		]
		if any(s):
			self._waf.append('ChinaCache Load Balancer (ChinaCache)')

	def Cloudflare(self):
		s = [
			self.header_check(('server', 'cloudflare')),
			self.header_check(('server', r'cloudflare[-_]nginx')),
			self.header_check(('cf-ray', r'.+?')),
			self.cookie_check('__cfduid')
		]
		if any(s):
			self._waf.append('Cloudflare (Cloudflare Inc.)')

	def w360WangZhanBao(self):
		s = [
			self.header_check(('Server', r'qianxin\-waf')),
			self.header_check(('WZWS-Ray', r'.+?')),
			self.header_check(('X-Powered-By-360WZB', r'.+?')),
			self.content_check(r'wzws\-waf\-cgi/'),
			self.content_check(r'wangshan\.360\.cn'),
			self.status_check(493)
		]
		if any(s):
			self._waf.append('360WangZhanBao (360 Technologies)')

	def Alert_Logic(self):
		s = [
			self.content_check(r'<(title|h\d{1})>requested url cannot be found'),
			self.content_check(r'we are sorry.{0,10}?but the page you are looking for cannot be found'),
			self.content_check(r'back to previous page'),
			self.content_check(r'proceed to homepage'),
			self.content_check(r'reference id'),
			]
		if all(i for i in s):
			self._waf.append('Alert Logic (Alert Logic)')

	def Janusec(self):
		s = [
			self.content_check(r'janusec application gateway')
		]
		if any(s):
			self._waf.append('Janusec Application Gateway (Janusec)')

	def pkSec(self):
		schema1 = [
			self.content_check(r'pk.?Security.?Module'),
			self.content_check(r'Security.Alert')
		]
		schema2 = [
			self.content_check(r'As this could be a potential hack attack'),
			self.content_check(r'A safety critical (call|request) was (detected|discovered) and blocked'),
			self.content_check(r'maximum number of reloads per minute and prevented access')
		]
		if any(i for i in schema2):
			self._waf.append('pkSecurity IDS (pkSec)')
		if all(i for i in schema1):
			self._waf.append('pkSecurity IDS (pkSec)')

	def PentestIt(self):
		s = [
			self.content_check(r'@?nemesida(\-security)?\.com'),
			self.content_check(r'Suspicious activity detected.{0,10}?Access to the site is blocked'),
			self.content_check(r'nwaf@'),
			self.status_check(222)
		]
		if any(s):
			self._waf.append('Nemesida (PentestIt)')

	def Microsoft(self):
		s = [
			self.content_check(r'The.{0,10}?(isa.)?server.{0,10}?denied the specified uniform resource locator \(url\)'),
		]
		if any(s):
			self._waf.append('ISA Server (Microsoft)')

	def CdnNs_WdidcNet(self):
		s = [
			self.content_check(r'cdnnswaf application gateway')
		]
		if any(s):
			self._waf.append('CdnNS Application Gateway (CdnNs/WdidcNet)')

	def Akamai(self):
		s = [
			self.header_check(('Server', 'AkamaiGHost')),
			self.header_check(('Server', 'AkamaiGHost'))        
		]
		if any(s):
			self._waf.append('Kona SiteDefender (Akamai)')

	def LimeLight(self):
		s = [
			self.cookie_check(r'^limelight'),
			self.cookie_check(r'^l[mg]_sessid=')
		]
		if any(s):
			self._waf.append('LimeLight CDN (LimeLight)')

	def AliYunDun(self):
		s = [
			self.content_check(r'error(s)?\.aliyun(dun)?\.(com|net)?'),
			self.cookie_check(r'^aliyungf_tc='),
			self.content_check(r'cdn\.aliyun(cs)?\.com'),
			self.status_check(405)
			]
		if all(i for i in s):
			self._waf.append('AliYunDun (Alibaba Cloud Computing)')

	def PerimeterX(self):
		s = [
			self.content_check(r'www\.perimeterx\.(com|net)/whywasiblocked'),
			self.content_check(r'client\.perimeterx\.(net|com)'),
			self.content_check(r'denied because we believe you are using automation tools')
		]
		if any(s):
			self._waf.append('PerimeterX (PerimeterX)')

	def RSJoomla(self):
		s = [
			self.content_check(r'com_rsfirewall_(\d{3}_forbidden|event)?')
		]
		if any(s):
			self._waf.append('RSFirewall (RSJoomla!)')

	def Greywizard(self):
		s = [
			self.header_check(('Server', 'greywizard')),
			self.content_check(r'<(title|h\d{1})>Grey Wizard'),
			self.content_check(r'contact the website owner or Grey Wizard'),
			self.content_check(r'We.ve detected attempted attack or non standard traffic from your ip address')
		]
		if any(s):
			self._waf.append('Greywizard (Grey Wizard)')

	def XLabs(self):
		s = [
			self.header_check(('X-CDN', r'XLabs Security')),
			self.header_check(('Secured', r'^By XLabs Security')),
			self.header_check(('Server', r'XLabs[-_]?.?WAF'))
		]
		if any(s):
			self._waf.append('XLabs Security WAF (XLabs)')

	def Incapsula(self):
		s = [
			self.cookie_check(r'^incap_ses.*?='),
			self.cookie_check(r'^visid_incap.*?='),
			self.content_check(r'incapsula incident id'),
			self.content_check(r'powered by incapsula'),
			self.content_check(r'/_Incapsula_Resource')
		]
		if any(s):
			self._waf.append('Incapsula (Imperva Inc.)')

	def Radware(self):
		schema1 = [
			self.content_check(r'CloudWebSec\.radware\.com'),
			self.header_check(('X-SL-CompState', '.+'))
		]
		schema2 = [
			self.content_check(r'because we have detected unauthorized activity'),
			self.content_check(r'<title>Unauthorized Request Blocked'),
			self.content_check(r'if you believe that there has been some mistake'),
			self.content_check(r'\?Subject=Security Page.{0,10}?Case Number')
		]
		if any(i for i in schema1):
			self._waf.append('AppWall (Radware)')
		if all(i for i in schema2):
			self._waf.append('AppWall (Radware)')

	def StackPath(self):
		s = [
			self.content_check(r"This website is using a security service to protect itself"),
			self.content_check(r'You performed an action that triggered the service and blocked your request')
		]
		if all(i for i in s):
			self._waf.append('StackPath (StackPath)')

	def Zenedge(self):
		s = [
			self.header_check(('Server', 'ZENEDGE')),
			self.header_check(('X-Zen-Fury', r'.+?')),
			self.content_check(r'/__zenedge/')
		]
		if any(s):
			self._waf.append('Zenedge (Zenedge)')

	def NewDefend(self):
		s = [
			# This header can be obtained without attack mode
			# Most reliable fingerprint
			self.header_check(('Server', 'Newdefend')),
			# Reliable ones within blockpage
			self.content_check(r'www\.newdefend\.com/feedback'),
			self.content_check(r'/nd\-block/')
		]
		if any(s):
			self._waf.append('Newdefend (NewDefend)')

	def ArmorLogic(self):
		s = [
			self.header_check(('Server', 'Profense')),
			self.cookie_check(r'^PLBSID=')
		]
		if any(s):
			self._waf.append('Profense (ArmorLogic)')

	def OWASP(self):
		s = [
			self.content_check(r'Request rejected by xVarnish\-WAF')
		]
		if any(s):
			self._waf.append('Varnish (OWASP)')

	def Puhui(self):
		s = [
			self.header_check(('Server', r'Puhui[\-_]?WAF'))
		]
		if any(s):
			self._waf.append('Puhui (Puhui)')

	def Sabre(self):
		schema1 = [
			self.content_check(r'dxsupport\.sabre\.com')
		]
		schema2 = [
			self.content_check(r'<title>Application Firewall Error'),
			self.content_check(r'add some important details to the email for us to investigate')
		]
		if any(i for i in schema1):
			self._waf.append('Sabre Firewall (Sabre)')
		if all(i for i in schema2):
			self._waf.append('Sabre Firewall (Sabre)')

	def Microsoft(self):
		s = [
			self.content_check(r'Request Validation has detected a potentially dangerous client input'),
			self.content_check(r'ASP\.NET has detected data in the request'),
			self.content_check(r'HttpRequestValidationException')
		]
		if any(s):
			self._waf.append('RequestValidationMode (Microsoft)')

	def Comodo_cWatch(self):
		s = [
			self.header_check(('Server', r'Protected by COMODO WAF(.+)?'))
		]
		if any(s):
			self._waf.append('Comodo cWatch (Comodo CyberSecurity)')

	def BIG_IP_Local_Traffic_Manager(self):
		s = [
			self.cookie_check('^bigipserver'),
			self.header_check(('X-Cnection', 'close'))
		]
		if any(s):
			self._waf.append('BIG-IP Local Traffic Manager (F5 Networks)')

	def AnYu(self):
		s = [
			self.content_check(r'anyu.{0,10}?the green channel'),
			self.content_check(r'your access has been intercepted by anyu')
			]
		if any(s):
			self._waf.append('AnYu (AnYu Technologies)')

	def GoDaddy(self):
		s = [
			self.content_check(r'GoDaddy (security|website firewall)')
		]
		if any(s):
			self._waf.append('GoDaddy Website Protection (GoDaddy)')

	def Airee(self):
		s = [
			self.header_check(('Server', 'Airee')),
			self.header_check(('X-Cache', r'(\w+\.)?airee\.cloud')),
			self.content_check(r'airee\.cloud')
		]
		if any(s):
			self._waf.append('AireeCDN (Airee)')

	def Barracuda(self):
		s = [
			self.cookie_check(r'^barra_counter_session='),
			self.cookie_check(r'^BNI__BARRACUDA_LB_COOKIE='),
			self.cookie_check(r'^BNI_persistence='),
			self.cookie_check(r'^BN[IE]S_.*?='),
			self.content_check(r'Barracuda.Networks')
		]
		if any(s):
			self._waf.append('Barracuda (Barracuda Networks)')

	def Safe3(self):
		s = [
			self.header_check(('Server', 'Safe3 Web Firewall')),
			self.header_check(('X-Powered-By', r'Safe3WAF/[\.0-9]+?')),
			self.content_check(r'Safe3waf/[0-9\.]+?')
		]
		if any(s):
			self._waf.append('Safe3 Web Firewall (Safe3)')

	def WebARX(self):
		s = [
			self.content_check(r"WebARX.{0,10}?Web Application Firewall"),
			self.content_check(r"www\.webarxsecurity\.com"),
			self.content_check(r'/wp\-content/plugins/webarx/includes/')
		]
		if any(s):
			self._waf.append('WebARX (WebARX Security Solutions)')

	def Yunaq(self):
		s = [
			self.content_check(r'www\.365cyd\.com'),
			self.content_check(r'help\.365cyd\.com/cyd\-error\-help.html\?code=403')
		]
		if any(s):
			self._waf.append('Chuang Yu Shield (Yunaq)')

	def PowerCDN(self):
		s = [
			self.header_check(('Via', r'(.*)?powercdn.com(.*)?')),
			self.header_check(('X-Cache', r'(.*)?powercdn.com(.*)?')),
			self.header_check(('X-CDN', r'PowerCDN'))
		]
		if any(s):
			self._waf.append('PowerCDN (PowerCDN)')

	def Oracle(self):
		s = [
			self.content_check(r'<title>fw_error_www'),
			self.content_check(r'src=\"/oralogo_small\.gif\"'),
			self.content_check(r'www\.oracleimg\.com/us/assets/metrics/ora_ocom\.js')
		]
		if any(s):
			self._waf.append('Oracle Cloud (Oracle)')

	def Barikode(self):
		s = [
			self.content_check(r'<strong>barikode<.strong>'),
		]
		if any(s):
			self._waf.append('Barikode (Ethic Ninja)')

	def UCloud(self):
		s = [
			self.header_check(('Server', r'uewaf(/[0-9\.]+)?')),
			self.content_check(r'/uewaf_deny_pages/default/img/'),
			self.content_check(r'ucloud\.cn')
		]
		if any(s):
			self._waf.append('UEWaf (UCloud)')

	def Eisoo(self):
		s = [
			self.header_check(('Server', r'EisooWAF(\-AZURE)?/?')),
			self.content_check(r'<link.{0,10}?href=\"/eisoo\-firewall\-block\.css'),
			self.content_check(r'www\.eisoo\.com'),
			self.content_check(r'&copy; \d{4} Eisoo Inc')
		]
		if any(s):
			self._waf.append('Eisoo Cloud Firewall (Eisoo)')

	def Teros(self):
		s = [
			self.cookie_check(r'^st8id=')
		]
		if any(s):
			self._waf.append('Teros (Citrix Systems)')

	def CloudLinux(self):
		s = [
			self.header_check(('Server', r'imunify360.{0,10}?')),
			self.content_check(r'protected.by.{0,10}?imunify360'),
			self.content_check(r'powered.by.{0,10}?imunify360'),
			self.content_check(r'imunify360.preloader')
		]
		if any(s):
			self._waf.append('Imunify360 (CloudLinux)')

	def SecKing(self):
		s = [
			self.header_check(('Server', r'secking(.?waf)?'))
		]
		if any(s):
			self._waf.append('SecKing (SecKing)')

	def Mission_Control_Shield(self):
		s = [
			self.header_check(('Server', 'Mission Control Application Shield'))
		]
		if any(s):
			self._waf.append('Mission Control Shield (Mission Control)')

	def BulletProof_Security_Pro(self):
		s = [
			self.content_check(r'\+?bpsMessage'),
			self.content_check(r'403 Forbidden Error Page'),
			self.content_check(r'If you arrived here due to a search')
		]
		if all(i for i in s):
			self._waf.append('BulletProof Security Pro (AITpro Security)')

	def CrawlProtect(self):
		s = [
			self.cookie_check(r'^crawlprotecttag='),
			self.content_check(r'<title>crawlprotect'),
			self.content_check(r'this site is protected by crawlprotect')
		]
		if any(s):
			self._waf.append('CrawlProtect (Jean-Denis Brun)')

	def Sophos(self):
		schema1 = [
			self.content_check(r'www\.sophos\.com'),
			self.content_check(r'Powered by.?(Sophos)? UTM Web Protection')
		]
		schema2 = [
			self.content_check(r'<title>Access to the requested URL was blocked'),
			self.content_check(r'Access to the requested URL was blocked'),
			self.content_check(r'incident was logged with the following log identifier'),
			self.content_check(r'Inbound Anomaly Score exceeded'),
			self.content_check(r'Your cache administrator is')
		]
		if any(i for i in schema1):
			self._waf.append('UTM Web Protection (Sophos)')
		if all(i for i in schema2):
			self._waf.append('UTM Web Protection (Sophos)')

	def Bekchy(self):
		s = [
			# Both signatures are contained within response, so checking for any one of them
			# Sometimes I observed that there is an XHR request being being made to submit the 
			# report data automatically upon page load. In those cases a missing https is causing
			# false negatives.
			self.content_check(r'Bekchy.{0,10}?Access Denied'),
			self.content_check(r'bekchy\.com/report')
		]
		if any(s):
			self._waf.append('Bekchy (Faydata Technologies Inc.)')

	def Beluga(self):
		s = [
			self.header_check(('Server', r'Beluga')),
			self.cookie_check(r'^beluga_request_trail=')
		]
		if any(s):
			self._waf.append('Beluga CDN (Beluga)')

	def NSFocus(self):
		s = [
			self.header_check(('Server', 'NSFocus'))
		]
		if any(s):
			self._waf.append('NSFocus (NSFocus Global Inc.)')

	def FirePass(self):
		schema1 = [
			self.cookie_check('^VHOST'),
			self.header_check(('Location', r'\/my\.logon\.php3'))
		]
		schema2 = [
			self.cookie_check(r'^F5_fire.+?'),
			self.cookie_check('^F5_passid_shrinked')
		]
		if all(i for i in schema1):
			self._waf.append('FirePass (F5 Networks)')
		if all(i for i in schema2):
			self._waf.append('FirePass (F5 Networks)')

	def RayWAF(self):
		s = [
			self.header_check(('Server', r'WebRay\-WAF')),
			self.header_check(('DrivedBy', r'RaySrv.RayEng/[0-9\.]+?'))
		]
		if any(s):
			self._waf.append('RayWAF (WebRay Solutions)')

	def WTS(self):
		s = [
			self.header_check(('Server', r'wts/[0-9\.]+?')),
			self.content_check(r"<(title|h\d{1})>WTS\-WAF")
		]
		if any(s):
			self._waf.append('WTS-WAF (WTS)')

	def Bluedon(self):
		s = [
			# Found sample servers returning 'Server: BDWAF/2.0'
			self.header_check(('Server', r'BDWAF')),
			self.content_check(r'bluedon web application firewall')
		]
		if any(s):
			self._waf.append('Bluedon (Bluedon IST)')

	def BeyondTrust(self):
		s = [
			self.content_check(r'SecureIIS is an internet security application'),
			self.content_check(r'Download SecureIIS Personal Edition'),
			self.content_check(r'https?://www\.eeye\.com/Secure\-?IIS')
		]
		if any(s):
			self._waf.append('eEye SecureIIS (BeyondTrust)')

	def Reblaze(self):
		schema1 = [
			self.cookie_check(r'^rbzid'),
			self.header_check(('Server', 'Reblaze Secure Web Gateway'))
		]
		schema2 = [
			self.content_check(r'current session has been terminated'),
			self.content_check(r'do not hesitate to contact us'),
			self.content_check(r'access denied \(\d{3}\)')
		]
		if any(i for i in schema1):
			self._waf.append('Reblaze (Reblaze)')
		if all(i for i in schema2):
			self._waf.append('Reblaze (Reblaze)')

	def West263CDN(self):
		s = [
			self.header_check(('X-Cache', r'WS?T263CDN'))
		]
		if any(s):
			self._waf.append('West263 CDN (West263CDN)')

	def Shield_Security(self):
		s = [
			self.content_check(r"You were blocked by the Shield"),
			self.content_check(r"remaining transgression\(s\) against this site"),
			self.content_check(r"Something in the URL.{0,5}?Form or Cookie data wasn\'t appropriate")
		]
		if any(s):
			self._waf.append('Shield Security (One Dollar Plugin)')

	def TrueShield(self):
		s = [
			self.content_check(r"SiteLock will remember you"),
			self.content_check(r"Sitelock is leader in Business Website Security Services"),
			self.content_check(r"sitelock[_\-]shield([_\-]logo|[\-_]badge)?"),
			self.content_check(r'SiteLock incident ID')
		]
		if any(s):
			self._waf.append('Sitelock (TrueShield)')

	def Incsub(self):
		schema1 = [
			self.content_check(r'href="http(s)?.\/\/wpmudev.com\/.{0,15}?'),
			self.content_check(r'Click on the Logs tab, then the WAF Log.'),
			self.content_check(r'Choose your site from the list'),
			self.status_check(403)
		]
		schema2 = [
			self.content_check(r'<h1>Whoops, this request has been blocked!'),
			self.content_check(r'This request has been deemed suspicious'),
			self.content_check(r'possible attack on our servers.'),
			self.status_check(403)
		]
		if all(i for i in schema1):
			self._waf.append('wpmudev WAF (Incsub)')
		if all(i for i in schema2):
			self._waf.append('wpmudev WAF (Incsub)')
	

	def Safeline(self):
		s = [
			self.content_check(r'safeline|<!\-\-\sevent id:')
		]
		if any(s):
			self._waf.append('Safeline (Chaitin Tech.)')

	def Microsoft(self):
		s = [
			self.content_check(r"Rejected[-_]By[_-]UrlScan"),
			self.content_check(r'A custom filter or module.{0,4}?such as URLScan')
		]
		if any(s):
			self._waf.append('URLScan (Microsoft)')

	def SiteGround(self):
		s = [
			self.content_check(r"Our system thinks you might be a robot!"),
			self.content_check(r'access is restricted due to a security rule')
		]
		if any(s):
			self._waf.append('SiteGround (SiteGround)')

	def DynamicWeb(self):
		s = [
			self.header_check(('X-403-Status-By', r'dw.inj.check')),
			self.content_check(r'by dynamic check(.{0,10}?module)?')
		]
		if any(s):
			self._waf.append('DynamicWeb Injection Check (DynamicWeb)')

	def DenyALL(self):
		s = [
			self.status_check(200),
			self.reason_check('Condition Intercepted')
		]
		if all(i for i in s):
			self._waf.append('DenyALL (Rohde & Schwarz CyberSecurity)')

	def Microsoft(self):
		s = [
			self.content_check(r'iis (\d+.)+?detailed error'),
			self.content_check(r'potentially dangerous request querystring'),
			self.content_check(r'application error from being viewed remotely (for security reasons)?'),
			self.content_check(r'An application error occurred on the server'),
		]
		if any(s):
			self._waf.append('ASP.NET Generic (Microsoft)')

	def Phion_Ergon(self):
		s = [
			# This method of detection is old (though most reliable), so we check it first
			self.cookie_check(r'^al[_-]?(sess|lb)='),
			self.content_check(r'server detected a syntax error in your request')
			]
		if any(s):
			self._waf.append('Airlock (Phion/Ergon)')

	def CacheFly(self):
		s = [
			self.header_check(('BestCDN', r'Cachefly')),
			self.cookie_check(r'^cfly_req.*=')
		]
		if any(s):
			self._waf.append('CacheFly CDN (CacheFly)')

	def DotDefender(self):
		s = [
			self.header_check(('X-dotDefender-denied', r'.+?')),
			self.content_check(r'dotdefender blocked your request'),
			self.content_check(r'Applicure is the leading provider of web application security')
		]
		if any(s):
			self._waf.append('DotDefender (Applicure Technologies)')

	def Cisco(self):
		s = [
			self.header_check(('Server', 'ACE XML Gateway'))
		]
		if any(s):
			self._waf.append('ACE XML Gateway (Cisco)')

	def NetContinuum(self):
		s = [
			self.cookie_check(r'^NCI__SessionId=')
		]
		if any(s):
			self._waf.append('NetContinuum (Barracuda Networks)')

	def BitNinja(self):
		s = [
			self.content_check(r'Security check by BitNinja'),
			self.content_check(r'Visitor anti-robot validation')
		]
		if any(s):
			self._waf.append('BitNinja (BitNinja)')

	def Sucuri_CloudProxy(self):
		s = [
			self.header_check(('X-Sucuri-ID', r'.+?')),
			self.header_check(('X-Sucuri-Cache', r'.+?')),
			self.header_check(('Server', r'Sucuri(\-Cloudproxy)?')),
			self.header_check(('X-Sucuri-Block', r'.+?')),
			self.content_check(r"Access Denied.{0,6}?Sucuri Website Firewall"),
			self.content_check(r"<title>Sucuri WebSite Firewall.{0,6}?(CloudProxy)?.{0,6}?Access Denied"),
			self.content_check(r"sucuri\.net/privacy\-policy"),
			self.content_check(r"cdn\.sucuri\.net/sucuri[-_]firewall[-_]block\.css"),
			self.content_check(r'cloudproxy@sucuri\.net')
		]
		if any(s):
			self._waf.append('Sucuri CloudProxy (Sucuri Inc.)')

	def Huawei(self):
		s = [
			self.cookie_check(r'^HWWAFSESID='),
			self.header_check(('Server', r'HuaweiCloudWAF')),
			self.content_check(r'hwclouds\.com'),
			self.content_check(r'hws_security@')
		]
		if any(s):
			self._waf.append('Huawei Cloud Firewall (Huawei)')

	def ServerDefender_VP(self):
		s = [
			self.header_check(('X-Pint', r'p(ort\-)?80'))
		]
		if any(s):
			self._waf.append('ServerDefender VP (Port80 Software)')

	def AdNovum(self):
		s = [
			self.cookie_check(r'^Navajo'),
			self.cookie_check(r'^NP_ID')
		]
		if any(s):
			self._waf.append('NevisProxy (AdNovum)')

	def Trafficshield(self):
		s = [
			self.cookie_check('^ASINFO='),
			self.header_check(('Server', 'F5-TrafficShield'))
		]
		if any(s):
			self._waf.append('Trafficshield (F5 Networks)')

	def DOSarrest(self):
		s = [
			self.header_check(('X-DIS-Request-ID', '.+')),
			# Found samples of DOSArrest returning 'Server: DoSArrest/3.5'
			self.header_check(('Server', r'DOSarrest(.*)?'))
		]
		if any(s):
			self._waf.append('DOSarrest (DOSarrest Internet Security)')

	def Astra(self):
		s = [
			self.cookie_check(r'^cz_astra_csrf_cookie'),
			self.content_check(r'astrawebsecurity\.freshdesk\.com'),
			self.content_check(r'www\.getastra\.com/assets/images')
		]
		if any(s):
			self._waf.append('Astra (Czar Securities)')

	def BIG_IP_AP_Manager(self):
		schema1 = [
			self.cookie_check('^LastMRH_Session'),
			self.cookie_check('^MRHSession')
		]
		schema2 = [
			self.cookie_check('^MRHSession'),
			self.header_check(('Server', r'Big([-_])?IP'))
		]
		schema3 = [
			self.cookie_check('^F5_fullWT'),
			self.cookie_check('^F5_fullWT'),
			self.cookie_check('^F5_HT_shrinked')
		]
		if all(i for i in schema1):
			self._waf.append('BIG-IP AP Manager (F5 Networks)')
		if all(i for i in schema2):
			self._waf.append('BIG-IP AP Manager (F5 Networks)')
		if any(i for i in schema3):
			self._waf.append('BIG-IP AP Manager (F5 Networks)')

	def MaxCDN(self):
		s = [
			self.header_check(('X-CDN', r'maxcdn'))
		]
		if any(s):
			self._waf.append('MaxCDN (MaxCDN)')

	def Inactiv(self):
		s = [
			self.content_check(r'firewall.{0,15}?powered.by.{0,15}?malcare.{0,15}?pro'),
			self.content_check('blocked because of malicious activities')
		]
		if any(s):
			self._waf.append('Malcare (Inactiv)')

	def BinarySec(self):
		s = [
			self.header_check(('Server', 'BinarySec')),
			self.header_check(('x-binarysec-via', '.+')),
			self.header_check(('x-binarysec-nocache', '.+'))
		]
		if any(s):
			self._waf.append('BinarySec (BinarySec)')

	def Varnish(self):
		s = [
			self.header_check(('Server', 'Varnish')),
			self.header_check(('X-Varnish', '.+')),
			self.header_check(('X-Cachewall-Action', '.+?')),
			self.header_check(('X-Cachewall-Reason', '.+?')),
			self.content_check(r'security by cachewall'),
			self.content_check(r'403 naughty.{0,10}?not nice!'),
			self.content_check(r'varnish cache server')
		]
		if any(s):
			self._waf.append('CacheWall (Varnish)')

	def FLOSS(self):
		schema1 = [
			self.header_check(('Server', r'^openresty/[0-9\.]+?')),
			self.status_check(403)
		]
		schema2 = [
			self.content_check(r'openresty/[0-9\.]+?'),
			self.status_check(406)
		]
		if all(i for i in schema1):
			self._waf.append('Open-Resty Lua Nginx (FLOSS)')
		if all(i for i in schema2):
			self._waf.append('Open-Resty Lua Nginx (FLOSS)')

	def HyperGuard(self):
		s = [
			self.cookie_check('^WODSESSION=')
		]
		if any(s):
			self._waf.append('HyperGuard (Art of Defense)')

	def Secure_Entry(self):
		s = [
			self.header_check(('Server', 'Secure Entry Server'))
		]
		if any(s):
			self._waf.append('Secure Entry (United Security Providers)')

	def Accenture(self):
		s = [
			self.header_check(('Server', r'ZScaler')),
			self.content_check(r"Access Denied.{0,10}?Accenture Policy"),
			self.content_check(r'policies\.accenture\.com'),
			self.content_check(r'login\.zscloud\.net/img_logo_new1\.png'),
			self.content_check(r'Zscaler to protect you from internet threats'),
			self.content_check(r"Internet Security by ZScaler"),
			self.content_check(r"Accenture.{0,10}?webfilters indicate that the site likely contains")
		]
		if any(s):
			self._waf.append('ZScaler (Accenture)')

	def BlockDoS(self):
		s = [
			self.header_check(('Server', r'blockdos\.net'))
		]
		if any(s):
			self._waf.append('BlockDoS (BlockDoS)')

	def SafeDog(self):
		s = [
			self.cookie_check(r'^safedog\-flow\-item='),
			self.header_check(('Server', 'Safedog')),
			self.content_check(r'safedogsite/broswer_logo\.jpg'),
			self.content_check(r'404\.safedog\.cn/sitedog_stat.html'),
			self.content_check(r'404\.safedog\.cn/images/safedogsite/head\.png')
		]
		if any(s):
			self._waf.append('Safedog (SafeDog)')

	def Yunjiasu(self):
		s = [
			self.header_check(('Server', r'Yunjiasu(.+)?'))
		]
		if any(s):
			self._waf.append('Yunjiasu (Baidu Cloud Computing)')

	def Cloudbric(self):
		s = [
			self.content_check(r'<title>Cloudbric.{0,5}?ERROR!'),
			self.content_check(r'Your request was blocked by Cloudbric'),
			self.content_check(r'please contact Cloudbric Support'),
			self.content_check(r'cloudbric\.zendesk\.com'),
			self.content_check(r'Cloudbric Help Center'),
			self.content_check(r'malformed request syntax.{0,4}?invalid request message framing.{0,4}?or deceptive request routing')
		]
		if any(s):
			self._waf.append('Cloudbric (Penta Security)')

	def Approach(self):
		s = [
			# This method of detection is old (though most reliable), so we check it first
			self.content_check(r'approach.{0,10}?web application (firewall|filtering)'),
			self.content_check(r'approach.{0,10}?infrastructure team')
			]
		if any(s):
			self._waf.append('Approach (Approach)')

	def NinTechNet(self):
		s = [
			self.content_check(r'<title>NinjaFirewall.{0,10}?\d{3}.forbidden'),
			self.content_check(r'For security reasons?.{0,10}?it was blocked and logged')
		]
		if all(i for i in s):
			self._waf.append('NinjaFirewall (NinTechNet)')

	def NetScaler_AppFirewall(self):
		s = [
			# This header can be obtained without attack mode
			self.header_check(('Via', r'NS\-CACHE')),
			# Cookies are set only when someone is authenticated.
			# Not much reliable since wafw00f isn't authenticating.
			self.cookie_check(r'^(ns_af=|citrix_ns_id|NSC_)'),
			self.content_check(r'(NS Transaction|AppFW Session) id'),
			self.content_check(r'Violation Category.{0,5}?APPFW_'),
			self.content_check(r'Citrix\|NetScaler'),
			# Reliable but not all servers return this header
			self.header_check(('Cneonction', r'^(keep alive|close)')),
			self.header_check(('nnCoection', r'^(keep alive|close)'))
		]
		if any(s):
			self._waf.append('NetScaler AppFirewall (Citrix Systems)')

	def NullDDoS(self):
		s = [
			self.header_check(('Server', r'NullDDoS(.System)?'))
		]
		if any(s):
			self._waf.append('NullDDoS Protection (NullDDoS)')

	def KnownSec(self):
		s = [
			self.content_check(r'/ks[-_]waf[-_]error\.png')
		]
		if any(s):
			self._waf.append('KS-WAF (KnownSec)')

	def Defiant(self):
		s = [
			self.header_check(('Server', r'wf[_\-]?WAF')),
			self.content_check(r"Generated by Wordfence"),
			self.content_check(r'broke one of (the )?Wordfence (advanced )?blocking rules'),
			self.content_check(r"/plugins/wordfence")
		]
		if any(s):
			self._waf.append('Wordfence (Defiant)')

	def SecuPress(self):
		s = [
			self.content_check(r'<(title|h\d{1})>SecuPress'),
		]
		if any(s):
			self._waf.append('SecuPress WP Security (SecuPress)')

	def Microsoft(self):
		s = [
			self.header_check(('X-Azure-Ref', '.+?')),
		]
		if any(s):
			self._waf.append('Azure Front Door (Microsoft)')

	def Qcloud(self):
		s = [
			self.content_check(r'腾讯云Web应用防火墙'),
			self.status_check(403)
			]
		if all(i for i in s):
			self._waf.append('Qcloud (Tencent Cloud)')
	

	def IBM(self):
		s = [
			self.header_check(('X-Backside-Transport', r'(OK|FAIL)'))
		]
		if any(s):
			self._waf.append('DataPower (IBM)')

	def TransIP(self):
		s = [
			self.header_check(('X-TransIP-Backend', '.+')),
			self.header_check(('X-TransIP-Balancer', '.+'))
		]
		if any(s):
			self._waf.append('TransIP Web Firewall (TransIP)')

	def ArvanCloud(self):
		s = [
			self.header_check(('Server', 'ArvanCloud'))
		]
		if any(s):
			self._waf.append('ArvanCloud (ArvanCloud)')

	def Dell(self):
		s = [
			self.header_check(('Server', 'SonicWALL')),
			self.content_check(r"<(title|h\d{1})>Web Site Blocked"),
			self.content_check(r'\+?nsa_banner')
		]
		if any(s):
			self._waf.append('SonicWall (Dell)')

	def SiteGuard(self):
		s = [
			self.content_check(r"Powered by SiteGuard"),
			self.content_check(r'The server refuse to browse the page')
		]
		if any(s):
			self._waf.append('SiteGuard (Sakura Inc.)')

	def IBM(self):
		s = [
			self.header_check(('Server', 'WebSEAL')),
			self.content_check(r"This is a WebSEAL error message template file"),
			self.content_check(r"WebSEAL server received an invalid HTTP request")
		]
		if any(s):
			self._waf.append('WebSEAL (IBM)')

	def Zecure(self):
		s = [
			self.content_check(r"<h\d{1}>\d{3}.forbidden<.h\d{1}>"),
			self.content_check(r"request forbidden by administrative rules")
		]
		if all(i for i in s):
			self._waf.append('Shadow Daemon (Zecure)')

	def Instart_DX(self):
		schema1 = [
			self.header_check(('X-Instart-Request-ID', '.+')),
			self.header_check(('X-Instart-Cache', '.+')),
			self.header_check(('X-Instart-WL', '.+'))
		]
		schema2 = [
			self.content_check(r'the requested url was rejected'),
			self.content_check(r'please consult with your administrator'),
			self.content_check(r'your support id is')
		]
		if any(i for i in schema1):
			self._waf.append('Instart DX (Instart Logic)')
		if all(i for i in schema2):
			self._waf.append('Instart DX (Instart Logic)')

	def Qiniu(self):
		s = [
			self.header_check(('X-Qiniu-CDN', r'\d+?'))
		]
		if any(s):
			self._waf.append('Qiniu (Qiniu CDN)')

	def Palo_Alto_Next_Gen_Firewall(self):
		s = [
			self.content_check(r'Download of virus.spyware blocked'),
			self.content_check(r'Palo Alto Next Generation Security Platform')
		]
		if any(s):
			self._waf.append('Palo Alto Next Gen Firewall (Palo Alto Networks)')

	def Fastly(self):
		s = [
			self.header_check(('X-Fastly-Request-ID', r'\w+'))
		]
		if any(s):
			self._waf.append('Fastly (Fastly CDN)')

	def EllisLab(self):
		s = [
			# I have seen some sites use a tracking header and sets a cookie upon authentication
			# 'Set-Cookie: _exp_tracking=rufyhweiuitefgcxyniercyft5-6dctuxeygfr'
			self.cookie_check(r'^exp_track.+?='),
			# There are traces found where cookie is returning values like:
			# Set-Cookie: exp_last_query=834y8d73y94d8g983u4shn8u4shr3uh3
			# Set-Cookie: exp_last_id=b342b432b1a876r8
			self.cookie_check(r'^exp_last_.+?='),
			# In-page fingerprints vary a lot in different sites. Hence these are not quite reliable.
			self.content_check(r'invalid get data')
		]
		if any(s):
			self._waf.append('Expression Engine (EllisLab)')

	def Wallarm(self):
		s = [
			self.header_check(('Server', r'nginx[\-_]wallarm'))
		]
		if any(s):
			self._waf.append('Wallarm (Wallarm Inc.)')

	def KeyCDN(self):
		s = [
			self.header_check(('Server', 'KeyCDN'))
		]
		if any(s):
			self._waf.append('KeyCDN (KeyCDN)')

	def Yundun(self):
		s = [
			self.header_check(('Server', 'YUNDUN')),
			self.header_check(('X-Cache', 'YUNDUN')),
			self.cookie_check(r'^yd_cookie='),
			self.content_check(r'Blocked by YUNDUN Cloud WAF'),
			self.content_check(r'yundun\.com/yd[-_]http[_-]error/'),
			self.content_check(r'www\.yundun\.com/(static/js/fingerprint\d{1}?\.js)?')
		]
		if any(s):
			self._waf.append('Yundun (Yundun)')

	def BlackBaud(self):
		s = [
			self.header_check(('X-Engine', 'onMessage Shield')),
			self.content_check(r'Blackbaud K\-12 conducts routine maintenance'),
			self.content_check(r'onMessage SHEILD'),
			self.content_check(r'maintenance\.blackbaud\.com'),
			self.content_check(r'status\.blackbaud\.com')
		]
		if any(s):
			self._waf.append('OnMessage Shield (BlackBaud)')

	def BIG_IP_AppSec_Manager(self):
		s = [
			self.content_check('the requested url was rejected'),
			self.content_check('please consult with your administrator')
		]
		if all(i for i in s):
			self._waf.append('BIG-IP AppSec Manager (F5 Networks)')

	def LiteSpeed(self):
		schema1 = [
			self.header_check(('Server', 'LiteSpeed')),
			self.status_check(403)
		]
		schema2 = [
			self.content_check(r'Proudly powered by litespeed web server'),
			self.content_check(r'www\.litespeedtech\.com/error\-page')
		]
		if all(i for i in schema1):
			self._waf.append('LiteSpeed (LiteSpeed Technologies)')
		if any(i for i in schema2):
			self._waf.append('LiteSpeed (LiteSpeed Technologies)')

	def Squarespace(self):
		s = [
			self.header_check(('Server', 'Squarespace')),
			self.cookie_check(r'^SS_ANALYTICS_ID='),
			self.cookie_check(r'^SS_MATTR='),
			self.cookie_check(r'^SS_MID='),
			self.cookie_check(r'SS_CVT='),
			self.content_check(r'status\.squarespace\.com'),
			self.content_check(r'BRICK\-\d{2}')
		]
		if any(s):
			self._waf.append('Squarespace (Squarespace)') 

	def Jiasule(self):
		s = [
			self.header_check(('Server', r'jiasule\-waf')),
			self.cookie_check(r'^jsl_tracking(.+)?='),
			self.cookie_check(r'__jsluid='),
			self.content_check(r'notice\-jiasule'),
			self.content_check(r'static\.jiasule\.com')
		]
		if any(s):
			self._waf.append('Jiasule (Jiasule)')
