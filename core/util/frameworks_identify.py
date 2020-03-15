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
from re import search

class main:

	def __init__(self, framework, content, headers):
		self.framework = framework
		self.content = content
		self.headers = headers
		self._frameworks = []

	def run_crawl(self):
		for i in dir(self):
			con1 = not i.startswith("__")
			con2 = not i.endswith("__")
			con3 = i not in ("_frameworks", "content", "headers",
							 "framework", "frameworks", "run_crawl")
			if con1 and con2 and con3:
				getattr(self, i)()

	def apachejackrabbit(self):
		M = False
		M |= search(
			r"<\w[^>]*(=\"\/_jcr_content\/){1}[^>]*\>", self.content) is not None
		if M:
			self._frameworks.append("Apache Jackrabbit/Adobe CRX repository")

	def asp_mvc(self):
		M = False
		for header in self.headers.items():
			M |= header[0] == "x-aspnetmvc-version"
			M |= header[0] == "x-aspnet-version"
			M |= search(
				r"asp.net|anonymousID=|chkvalues=|__requestverificationtoken", header[1]) is not None
			if M:
				break
		M |= search(r"Web Settings for Active Server Pages",
					   self.content) is not None
		M |= search(
			r"name=\"__VIEWSTATEENCRYPTED\" id=\"__VIEWSTATEENCRYPTED\"", self.content) is not None
		if M:
			self._frameworks.append("ASP.NET Framework")

	def cakephp(self):
		M = False
		for header in self.headers.items():
			M |= search(r"CAKEPHP=", header[1]) is not None
			if M:
				break
		if M:
			self._frameworks.append("CakePHP - PHP Framework")

	def cherrypy(self):
		M = False
		for header in self.headers.items():
			M |= search(r"CherryPy", header[1]) is not None
			if M:
				break
		if M:
			self._frameworks.append("CherryPy - Python Framework")

	def codeigniter(self):
		M = False
		for header in self.headers.items():
			M |= search(r"ci_session=", header[1]) is not None
			if M:
				break
		if M:
			self._frameworks.append("CodeIgniter - PHP Framework")

	def dancer(self):
		M = False
		for header in self.headers.items():
			M |= search(r"Dancer|dancer.session=", header[1]) is not None
			if M:
				break
		if M:
			self._frameworks.append("Dancer - Perl Framework")

	def django(self):
		M = False
		for header in self.headers.items():
			M |= search(r"wsgiserver/", header[1]) is not None
			M |= search(r"python/", header[1]) is not None
			M |= search(r"csrftoken=", header[1]) is not None
			if M:
				break
		M |= search(
			r"\<meta name\=\"robots\" content\=\"NONE,NOARCHIVE\"\>\<title\>Welcome to Django\<\/title\>", self.content) is not None
		if M:
			self._frameworks.append("Django - Python Framework")

	def flask(self):
		M = False
		for header in self.headers.items():
			M |= search(r"flask", header[1]) is not None
			if M:
				break
		if M:
			self._frameworks.append("Flask - Python Framework")

	def fuelphp(self):
		M = False
		for header in self.headers.items():
			M |= search(r"fuelcid=", header[1]) is not None
			if M:
				break
		M |= search(
			r"Powered by \<a href\=\"http://fuelphp.com\"\>FuelPHP\<\/a\>", self.content) is not None
		if M:
			self._frameworks.append("FuelPHP - PHP Framework")

	def grails(self):
		M = False
		for header in self.headers.items():
			M |= search(r"grails", header[1]) is not None
			M |= search(r"x-grails", header[0]) is not None
			M |= search(r"x-grails-cached", header[0]) is not None
			if M:
				break
		if M:
			self._frameworks.append("Grails - Java Framework")

	def horde(self):
		M = False
		for header in self.headers:
			M |= search(r"webmail_version=|webmail4prod=",
						   header[1]) is not None
			if M:
				break
		M |= search(
			r"title\=\"This site is powered by The Horde Application Framework.\" href\=\"http://horde.org\"\>", self.content) is not None
		M |= search(
			r"Powered by \<\/font\>\<a href\=\"http://www.horde.org/\" TARGET\=_blank>", self.content) is not None
		M |= search(
			r"/themes/graphics/horde-power1.png\" alt\=\"Powered by Horde\" title\=\"\" \/\>", self.content) is not None
		M |= search(r"\<html\>\<body bgcolor\=\"\#aaaaaa\"\>\<a href\=\"icon_browser.php\"\>Application List\<\/a\>\<br \/\>\<br \/\>\<h2\>Icons for My Account\<\/h2\>", self.content) is not None
		M |= search(
			r"\<script language\=\"JavaScript\" type\=\"text/javascript\" src\=\"/hunter/js/enter_key_trap.js\"\>\<\/script\>", self.content) is not None
		M |= search(
			r"\<link href\=\"/mail/mailbox.php\?mailbox\=INBOX\" rel\=\"Top\" \/\>", self.content) is not None
		if M:
			self._frameworks.append("Horde - PHP Framework")

	def karrigell(self):
		M = False
		for header in self.headers.items():
			M |= search(r"karrigell", header[1]) is not None
			if M:
				break
		if M:
			self._frameworks.append(r"Karrigell - Python Framework")

	def larvel(self):
		M = False
		for header in self.headers.items():
			M |= search(r"laravel_session=", header[1]) is not None
			if M:
				break
		if M:
			self._frameworks.append("Larvel - PHP Framework")

	def nette(self):
		M = False
		for header in self.headers:
			M |= search(r"Nette Framework|Nette|nette-browser=",
						   header[1])is not None
			if M:
				break
		if M:
			self._frameworks.append("Nette - PHP Framework")

	def phalcon(self):
		M = False
		for header in self.headers:
			M |= search(r"phalcon-auth-|phalconphp.com|phalcon",
						   header[1])is not None
			if M:
				break
		if M:
			self._frameworks.append("Phalcon - PHP Framework")

	def play(self):
		M = False
		for header in self.headers.items():
			M |= search(r"play! framework;", header[1]) is not None
			if M:
				break
		if M:
			self._frameworks.append("Play - Java Framework")

	def rails(self):
		M = False
		for header in self.headers.items():
			M |= search(r"phusion passenger", header[1]) is not None
			M |= search(r"rails", header[1]) is not None
			M |= search(r"_rails_admin_session=", header[1]) is not None
			M |= search(r"x-rails", header[0]) is not None
			if M:
				break
		M |= search(
			r"\<meta content\=\"authenticity_token\" name\=\"csrf-param\"\s?\/>\s?\<meta content=\"[^\"]{44}\" name\=\"csrf-token\"\s?\/>", self.content) is not None
		M |= search(
			r"\<link[^>]*href\=\"[^\"]*\/assets\/application-?\w{32}?\.css\"", self.content) is not None
		M |= search(
			r"\<script[^>]*\/assets\/application-?\w{32}?\.js\"", self.content) is not None
		if M:
			self._frameworks.append("Ruby on Rails - Ruby Framework")

	def seagull(self):
		M = False
		M |= search(
			r"<meta name\=\"generator\" content\=\"Seagull Framework\" \/\>", self.content) is not None
		M |= search(
			r"Powered by \<a href\=\"http:\/\/seagullproject.org[\/]*\" title\=\"Seagull framework homepage\"\>Seagull PHP Framework<\/a\>", self.content) is not None
		M |= search(r"var SGL_JS_SESSID[\s]*=", self.content) is not None
		if M:
			self._frameworks.append("Seagull - PHP Framework")

	def spring(self):
		M = False
		for header in self.headers:
			M |= search(
				r"org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=", header[1]) is not None
			if M:
				break
		if M:
			self._frameworks.append("Spring Framework (Java Platform)")

	def symfony(self):
		M = False
		M |= search(r"\"powered by symfony\"", self.content) is not None
		M |= search(
			r"Powered by \<a \href\=\"http://www.symfony-project.org/\"\>", self.content) is not None
		if M:
			self._frameworks.append("Symfony - PHP Framework")

	def web2py(self):
		M = False
		for header in self.headers.items():
			M |= search(r"web2py", header[1]) is not None
			if M:
				break
		M |= search(r"\<div id\=\"serendipityLeftSideBar\"\>",
					   self.content) is not None
		if M:
			self._frameworks.append("Web2Py - Python Framework")

	def yii(self):
		M = False
		M |= search(
			r"\<a href\=\"http://www.yiiframework.com/\" rel\=\"external\"\>Yii Framework\<\/a\>", self.content) is not None
		M |= search(r"\>Yii Framework\<\/a\>", self.content) is not None
		if M:
			self._frameworks.append("Yii - PHP Framework")

	def zend(self):
		M = False
		for header in self.headers.items():
			M |= search(r"zend", header[1]) is not None
			if M:
				break
		M |= search(
			r"\<meta name\=\"generator\" content\=\"Zend.com CMS ([\d\.]+)\"", self.content) is not None
		M |= search(
			r"<meta name\=\"vendor\" content\=\"Zend Technologies", self.content) is not None
		M |= search(r"\"Powered by Zend Framework\"",
					   self.content) is not None
		M |= search(r" alt\=\"Powered by Zend Framework!\" \/\>",
					   self.content) is not None
		if M:
			self._frameworks.append("Zend - PHP Framework")

	def yoast(self):
		M = search(
			r"<!-- This site is optimized with the Yoast SEO Premium plugin v([0-9]+.[0-9]+.[0-9]+) - https://yoast\.com/wordpress/plugins/seo/ -->", self.content)
		if M:
			self._frameworks.append("Yoast SEO v" + M.group(1))

	@property
	def frameworks(self):
		return self._frameworks
