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

	def __init__(self, content, headers):
		""" baidu.com search engine

			content	  : Web content
			headers	  : Web headers
		"""
		self.content = content
		self.headers = headers
		self._cms = None

	def run_crawl(self):
		for attr in dir(self):
			con1 = not attr.startswith('__')
			con2 = not attr.endswith('__')
			con3 = attr not in ('_cms', 'content', 'headers',
							 'cms', 'run_crawl', 'framework', 'initialize')
			if con1 and con2 and con3:
				getattr(self, attr)()
		
	def adobeaem(self):
		M = False
		M = search(
			r"<link[^>]*stylesheet[^>]*etc\/designs\/[^>]*\>[^<]*", self.content, I) is not None
		M |= search(
			r"<link[^>]*etc\/clientlibs\/[^>]*\>[^<]*", self.content, I) is not None
		M |= search(
			r"<script[^>]*etc\/clientlibs\/[^>]*\>[^<]*", self.content, I) is not None
		M |= search(
			r"<script[^>]*\/granite\/[^>]*(\.js\")+\>[^<]*", self.content, I) is not None
		if M:
			self._cms = 'Adobe AEM: Stack is based on Apache Sling + Apache Felix OSGi container + JCR Repo + Java'

	def drupal(self):
		M = False
		regexs = [r"\<script type\=\"text\/javascript\" src\=\"[^\"]*\/misc\/drupal.js[^\"]*\"\>\<\/script\>",
				  r"<[^>]+alt\=\"Powered by Drupal, an open source content management system\"",
				  r"@import \"[^\"]*\/misc\/drupal.css\"",
				  r"jQuery.extend\(drupal\.S*",
				  r"Drupal.extend\(\S*",
				  r"name=\"?generator\"? content=\"?Varbase",
				  r"jQuery.extend\(drupal\.S*",
				  r"data-drupal-selector=",
				  r"name=\"?generator\"? content=\"?Drupal ([0-9]+)",
				  ]
		if 'set-cookie' in self.headers.keys():
			if search(r"SESS[a-z0-9]{32}=[a-z0-9]{32}", self.headers["set-cookie"], I):
				M = "Drupal"
		if 'x-drupal-cache' in self.headers.keys():
			M = "Drupal"
		for i in regexs:
			tmp_M = search(i, self.content)
			if tmp_M:
				try:
					M = "Drupal version " + tmp_M.group(1)
				except IndexError:
					M = "Drupal"
				break
		if M:
			self._cms = M

	def joomla(self):
		M = False
		if 'set-cookie' in self.headers.keys():
			M |= search(
				r"mosvisitor=", self.headers["set-cookie"], I) is not None
		M |= search(
			r"\<meta name\=\"Generator\" content\=\"Joomla! - Copyright \(C\) 200[0-9] - 200[0-9] Open Source Matters. All rights reserved.\" \/\>", self.content, I) is not None
		M |= search(
			r"\<meta name\=\"generator\" content\=\"Joomla! (\d\.\d) - Open Source Content Management\" \/\>", self.content, I) is not None
		M |= search(
			r"Powered by \<a href\=\"http://www.joomla.org\"\>Joomla!\<\/a\>.", self.content, I) is not None
		if M:
			self._cms = 'Joomla'

	def magento(self):
		M = False
		if 'set-cookie' in self.headers.keys():
			M |= search(r"magento=[0-9a-f]+|frontend=[0-9a-z]+",
						   self.headers["set-cookie"], I) is not None
		M |= search(
			r"images/logo.gif\" alt\=\"Magento Commerce\" \/\>\<\/a\>\<\/h1\>", self.content, I) is not None
		M |= search(
			r"\<a href\=\"http://www.magentocommerce.com/bug-tracking\" id\=\"bug_tracking_link\"\>\<strong\>Report All Bugs\<\/strong\>\<\/a\>", self.content, I) is not None
		M |= search(
			r"\<link rel\=\"stylesheet\" type\=\"text/css\" href\=\"[^\"]+\/skin\/frontend\/[^\"]+\/css\/boxes.css\" media\=\"all\"", self.content, I) is not None
		M |= search(
			r"\<div id\=\"noscript-notice\" class\=\"magento-notice\"\>", self.content, I) is not None
		M |= search(
			r"Magento is a trademark of Magento Inc. Copyright &copy; ([0-9]{4}) Magento Inc", self.content, I) is not None
		if(M):
			self._cms = 'Magento'

	def plone(self):
		M = False
		if 'x-caching-rule-id' in self.headers.keys():
			M |= search(r"plone-content-types",
						   self.headers["x-caching-rule-id"], I) is not None
		if 'x-cache-rule' in self.headers.keys():
			M |= search(r"plone-content-types",
						   self.headers["x-cache-rule"], I) is not None
		M |= search(
			r"\<meta name\=\"generator\" content\=\"[^>]*http:\/\/plone.org\" \/>", self.content, I) is not None
		M |= search(
			r"(@import url|text\/css)[^>]*portal_css\/.*plone.*css(\)|\")", self.content, I) is not None
		M |= search(
			r"src\=\"[^\"]*ploneScripts[0-9]+.js\"", self.content, I) is not None
		M |= search(
			r"\<div class\=\"visualIcon contenttype-plone-site\"\>", self.content, I) is not None
		if(M):
			self._cms = "Plone"

	def silverstripe(self):
		M = False
		if 'set-cookie' in self.headers.keys():
			M |= search(
				r"PastVisitor=[0-9]+.*", self.headers["set-cookie"], I) is not None
		M |= search(
			r"\<meta name\=\"generator\"[^>]*content\=\"SilverStripe", self.content, I) is not None
		M |= search(
			r"\<link[^>]*stylesheet[^>]*layout.css[^>]*\>[^<]*\<link[^>]*stylesheet[^>]*typography.css[^>]*\>[^<]*\<link[^>]*stylesheet[^>]*form.css[^>]*\>", self.content, I) is not None
		M |= search(
			r"\<img src\=\"\/assets\/[^\/]+\/_resampled\/[^\"]+.jpg\"", self.content, I) is not None
		if(M):
			self._cms = "SilverStripe"

	def wordpress(self):
		M = False
		M |= search(
			r"\<meta name\=\"generator\" content\=\"WordPress.com\" \/\>", self.content, I) is not None
		M |= search(
			r"\<a href\=\"http://www.wordpress.com\"\>Powered by WordPress\<\/a\>", self.content, I) is not None
		M |= search(r"\<link rel\=\'https://api.w.org/\'",
					   self.content, I) is not None
		M |= search(r"\/wp-content\/plugins\/", self.content, I) is not None
		if M:
			self._cms = "WordPress"

	def concrete5(self):
		M = False
		M = search(
			r'<meta name="generator" content="concrete5',
			self.content) is not None
		M |= search(r'/packages/concrete5_theme/themes/',
					   self.content) is not None
		if M:
			self._cms = 'Concrete5'

	def typo3(self):
		M = False
		M = search(
			r'This website is powered by TYPO3|/typo3conf',
			self.content) is not None
		M |= search(
			r'"generator" content="TYPO3 CMS">|/typo3temp/assets/',
			self.content) is not None
		if M:
			self._cms = 'TYPO3'

	def hubspot(self):
		M = False
		M = search(
			r"<meta name=\"generator\" content=\"HubSpot\">", self.content) is not None
		M2 = search(
			r"<!-- Generated by the HubSpot Template Builder - template version ([0-9]{1,6}\.[0-9]{1,6}) -->", self.content)
		alert = "HubSpot"
		if M2:
			M |= True
			alert = f"HubSpot version {M2.group(1)}"
		if M:
			self._cms = alert

	def squarespace(self):
		M = False
		M = search(r"<!-- This is Squarespace. -->",
					  self.content) is not None
		if M:
			self._cms = 'Squarespace'
			
	def prestashop(self):
		M = False
		if 'set-cookie' in self.headers.keys():
			M |= search(r"PrestaShop-[a-z0-9A-Z]+", self.headers["set-cookie"], I) is not None
		if 'Powered-By' in self.headers.keys():
			M |= search(r"^Prestashop$",self.headers["Powered-By"], I) is not None
		M |= search(r"<a.*Ecommerce software by PrestaShop™[\s]*</a>", self.content) is not None
		if M:
			self._cms = 'Prestashop'

	@property
	def cms(self):
		return self._cms
