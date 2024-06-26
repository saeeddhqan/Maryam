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

meta = {
	'name': 'Find Social Networks',
	'author': 'Saeed',
	'version': '1.5',
	'description': 'Search to find Usernames in social networks.',
	'sources': ('bing', 'google', 'startpage', 'urlscan'),
	'options': (
		('query', None, True, 'Company Name or Query', '-q', 'store', str),
		('engines', 'google,bing', False, 'Search engine names. e.g `bing,google,..`', '-e', 'store', str),
		('url', None, False, 'The second source to crawl for', '-u', 'store', str),
		('depth', 1, False, 'Scraper depth level(default=1)(Only if the url is set)', '-d', 'store', int),
		('cthread', 5, False, 'The number of links that open per round(default=5)(Only if the url is set)', '-T', 'store', int),
		('limit', 5, False, 'Search limit(number of pages, default=5)', '-l', 'store', int),
		('count', 100, False, 'number of results per page(min=10, max=100, default=100)', '-c', 'store', int),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('social_nets -q microsoft -e google,bing,yahoo -c 50 -t 3 --output',
		'social_nets -q microsoft -e google',
		'social_nets -q microsoft -u microsoft.com -e google,bing,yahoo, -c 50 -t 5 -T 10 -d 2')
}

PAGES = ''
def search(self, name, q, q_formats, limit, count):
	global PAGES
	engine = getattr(self, name)
	eng = name
	varnames = engine.__init__.__code__.co_varnames
	if 'limit' in varnames and 'count' in varnames:
		attr = engine(q, limit, count)
	elif 'limit' in varnames:
		reg_dom = self.reglib().domain_m
		if eng == 'urlscan':
			if not re.search(reg_dom, q):
				self.verbose('Invalid domain name. Cannot run urlscan')
				return
			else:
				attr = engine(q, limit)
	else:
		attr = engine(q)

	attr.run_crawl()
	PAGES += attr.pages

def module_api(self):
	global PAGES
	query = '@' + self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	url = self.options['url']
	depth = self.options['depth']
	crawl_thread = self.options['cthread']
	engines = self.options['engines'].lower().split(',')
	page = ''
	try:
		if '.' in self.options['query']:
			page = self.request(self.options['query']).text
	except:
		page = ''
	PAGES += page
	self.thread(search, self.options['thread'], engines, query, {}, limit, count, meta['sources'])
	if url:
		scrap = self.web_scrap(url, False, depth, crawl_thread)
		scrap.run_crawl()
		PAGES += scrap.pages
	usernames = self.page_parse(PAGES).get_networks
	self.save_gather(usernames, 'osint/social_nets', query, output=self.options['output'])
	return usernames

def module_run(self):
	usernames = module_api(self)
	for net in usernames:
		lst = list(set(usernames[net]))
		if lst != []:
			self.alert(net)
			for atom in lst:
				self.output(f"\t{atom}", 'G')
