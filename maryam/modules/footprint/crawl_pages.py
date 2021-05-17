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

import re

meta = {
	'name' : 'Regex Web Search',
	'author' : 'Saeed',
	'version' : '0.6',
	'description' : 'Search to find keywords, emails, usernames, errors, meta tags and regex on the page/pages.',
	'options' : (
		('domain', None, True, 'Domain string', '-d', 'store', str),
		('regex', None, True, 'Regex or string for search in the pages', '-r', 'store', str),
		('more', False, False, 'Extract more information from the pages', '--more', 'store_true', bool),
		('limit', 1, False, 'Scraper depth level(default=1)', '-l', 'store', int),
		('debug', False, False, 'debug the scraper', '--debug', 'store_true', bool),
		('thread', 1, False, 'The number of links that open per round', '-t', 'store', int),
	),
	'examples': ('crawl_pages -d <DOMAIN> -r "https?://[A-z0-9\./]+"\
	 --output', 'crawl_pages -d <DOMAIN> --limit 2 --more')
}

def module_api(self):
	domain = self.options['domain']
	regex = self.options['regex']
	print(regex)
	try:
		re.compile(regex)
	except Exception as e:
		self.error(e, 'crawl_pages', 'module_api')
		return
	scrap = self.web_scrap(domain, self.options['debug'], self.options['limit'], self.options['thread'])
	scrap.run_crawl()
	pages = scrap.pages
	category_pages = scrap.category_pages
	# Output flag
	flag = 0
	resp = {}
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
			self.output(f"\tRegex {regex} search at {page}:")
			resp[regex].update({page : founds})
			for i in founds:
				if i not in reg_find.keys():
					reg_find[i] = 1
				else:
					reg_find[i] = reg_find[i] + 1

			for i in reg_find:
				self.output(f"\t\tFound '{i}' Repeated {reg_find[i]} times", 'G')
			if reg_find:
				if not flag:
					flag = 1
			reg_find = {}

		if not flag:
			self.output(f"\tNo response\n")


	if not self.options['more']:
		self.save_gather(resp, 'footprint/crawl_pages', domain, output=self.options['output'])
		return resp
	resp[regex]['more'] = {}

	page_parse = self.page_parse(pages)

	get_meta = page_parse.get_metatags
	resp[regex]['more']['meta'] = get_meta
	for key,attrs in enumerate(get_meta):
		self.alert(f"META {key}:")
		for attr_name in attrs:
			print(attr_name, attrs[attr_name])
			self.output(f"\t{attr_name} : {attrs[attr_name]}")

	## EMAILS ##
	############
	emails = page_parse.all_emails
	if emails != []:
		self.alert('Emails:')
		for i in emails:
			self.output(f"\t'{i}'", 'G')
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
				users.append(link)
				self.output(f"\t{str(link)}", 'G')
	resp[regex]['more']['usernames'] = users

	self.save_gather(resp, 'footprint/crawl_pages', domain, [regex, 'more'], output=self.options['output'])
	return resp

def module_run(self):
	module_api(self)