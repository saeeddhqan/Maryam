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

class Module(BaseModule):

	meta = {
		'name' : 'Crawler Pages',
		'author' : 'Saeeddqn',
		'version' : '0.6',
		'description' : 'Search to find keywords, emails, usernames, errors, meta tags and regex on the page/pages.',
		'options' : (
			('domain', BaseModule._global_options['target'], True, 'Domain string', '-d', 'store'),
			('regex', None, True, 'Regex or string for search in the pages', '-r', 'store'),
			('more', False, False, 'Extract more information from the pages', '--more', 'store_true'),
			('limit', 1, False, 'Scraper depth level(default=1)', '-l', 'store'),
			('debug', False, False, 'debug the scraper', '--debug', 'store_true'),
			('thread', 1, False, 'The number of links that open per round', '-t', 'store'),
			('output', False, False, 'Save output to workspace', '--output', 'store_true'),
		),
		'examples': ('crawl_pages -d <DOMAIN> -r "https?://[A-z0-9\./]+" --output', 'crawl_pages -d <DOMAIN> --crawl --more')
	}

	def module_run(self):
		domain = self.options['domain']
		regex = self.options['regex']
		try:
			re.compile(regex)
		except Exception as e:
			self.error(e)
			return
		scrap = self.web_scrap(domain, self.options['debug'], self.options['limit'], self.options['thread'])
		scrap.run_crawl()
		pages = scrap.pages
		category_pages = scrap.category_pages
		# Output flag
		flag = 0
		resp = {}
		output = self.options['output']
		methods = []
		resp[regex] = {}
		out = []
		## Regular Expression Search ##
		###############################
		if regex:
			reg_find = {}
			self.alert('Regex search:')
			regex_cmp = re.compile(regex)
			for page in category_pages:
				founds = regex_cmp.findall(category_pages[page])
				self.output(f'\tRegex {regex} search at {page}:')
				resp[regex].update({page : founds})
				for i in founds:
					if i not in reg_find.keys():
						reg_find[i] = 1
					else:
						reg_find[i] = reg_find[i] + 1

				for i in reg_find:
					self.output(f"\t\tFound '{i}' Repeated {reg_find[i]} times", 'g')
				if reg_find:
					if not flag:flag = 1
				reg_find = {}

			if not flag:
				self.output(f'\tNo response\n')


		if not self.options['more']:
			self.save_gather(resp, 'footprint/crawl_pages', domain, output=self.options['output'])
			return
		resp[regex]["more"] = {}
		methods.append("more")
		patterns = ["</HEAD><BODY><HR><H3>Error Occurred While Processing Request</H3><P>",
					"exceptions.ValueError",
					"<h2> <i>Runtime Error</i> </h2></span>",
					"<p>Active Server Pages</font> <font face=\"Arial\" size=2>error \'ASP 0126\'</font>",
					"<H3>Original Exception: </H3>",
					"<b> Description: </b>An unhandled exception occurred during the execution of the",
					"<H1>Error page exception</H1>",
					"<h2> <i>Access is denied</i> </h2></span>",
					"Server object error",
					"invalid literal for int()",
					"\[an error occurred while processing this directive\]",
					"<font face=\"Arial\" size=2>error \'800a0005\'</font>",
					"<HTML><HEAD><TITLE>Error Occurred While Processing Request</TITLE>",
					"\[java.lang.",
					"class java.lang.",
					"java.lang.NullPointerException",
					"java.rmi.ServerException",
					"at java.lang.",
					"onclick=\"toggle(\'full exception chain stacktrace\')",
					"at org.apache.catalina",
					"at org.apache.coyote.",
					"at org.apache.tomcat.",
					"at org.apache.jasper.",
					"<html><head><title>Application Exception</title>",
					"<p>Microsoft VBScript runtime </font>",
					"<font face=\"Arial\" size=2>error '800a000d'</font>",
					"<TITLE>nwwcgi Error",
					"\] does not contain handler parameter named",
					"PythonHandler django.core.handlers.modpython",
					"t = loader.get_template(template_name) # You need to create a 404.html template.",
					"<h2>Traceback <span>(innermost last)</span></h2>",
					"<h1 class=\"error_title\">Ruby on Rails application could not be started</h1>",
					"</b> on line <b>"
					"<title>Error Occurred While Processing Request</title></head><body><p></p>",
					"<TR><TD><H4>Error Diagnostic Information</H4><P><P>",
					"<li>Search the <a href=\"http://www.macromedia.com/support/coldfusion/\"",
					"target=\"new\">Knowledge Base</a> to find a solution to your problem.</li>",
					"thrown in <b>",
					"<h2 style=\"font:8pt/11pt verdana; color:000000\">HTTP 403.6 - Forbidden: IP address rejected<br>",
					"<TITLE>500 Internal Server Error</TITLE>",
					"<b>warning</b>[/]\w\/\w\/\S*",
					"<b>Fatal error</b>:",
					"<b>Warning</b>:",
					"open_basedir restriction in effect",
					"eval()'d code</b> on line <b>",
					"Server.Execute Error",
					"Fatal error</b>:  preg_replace",
					"<HTML><HEAD><TITLE>Error Occurred While Processing Request</TITLE></HEAD><BODY><HR><H3>",
					"Stack trace:"]

		page_parse = self.page_parse(pages)

		resp[regex]['more']['meta'] = {}
		get_meta = page_parse.get_metatags
		for key,attrs in enumerate(get_meta):
			self.alert(f'META {key}:')
			for attr_name in attrs:
				self.output(f'\t{attr_name} : {attrs[attr_name]}')

		## EMAILS ##
		############
		emails = page_parse.all_emails
		if emails != []:
			self.alert('Emails:')
			for i in emails:
				self.output(f"\t'{i}'", 'g')
		resp[regex]['more']['emails'] = emails

		## SOCIAL NETWORK ##
		####################
		usernames = page_parse.get_networks
		users = []
		self.alert('Social Networks:')
		for net in usernames:
			lst = list(set(usernames[net]))
			if lst != []:
				self.alert(net)
				for link in lst:
					if type(link) is tuple:
						link = list(link)
						for mic in link:
							if len(mic) > 2 and mic != '':
								users.append(mic)
								self.output(f'\t{str(mic)}', 'G')
					else:
						users.append(link)
						self.output(f'\t{str(link)}', 'G')
		resp[regex]['more']['social_networks'] = users

		flag = 0
		## ERRORS ##
		############
		resp[regex]['more']['errors'] = {}
		self.alert('Errors:')
		for page in category_pages:
			resp[regex]['more']['errors'][page] = []
			for patt in patterns:
				if re.search(patt, category_pages[page]):
					self.output(f"\t'{patt}' found at {page}", 'g')
					resp[regex]['more']['errors'][page].append(patt)
					if not flag:
						flag = 1

		if not flag:
			self.output('\t..')

		self.save_gather(resp, 'footprint/crawl_pages', domain, output=self.options['output'])
