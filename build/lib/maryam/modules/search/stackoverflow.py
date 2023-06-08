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
	'name': 'Stackoverflow Search',
	'author': 'Sanjiban Sengupta',
	'version': '0.5',
	'description': 'Search your query in the stackoverflow.com and show the results.',
	'sources': ('google', 'carrot2', 'bing', 'yahoo', 'millionshort', 'qwant', 'duckduckgo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store', int),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
		('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store', str),
	),
	'examples': ('stackoverflow -q "syntax error" -l 15 --output',)
}

LINKS = []
PAGES = ''

def search(self, name, q, q_formats, limit, count):
	global PAGES,LINKS
	engine = getattr(self, name)
	q = q_formats[f"{name}_q"] if f"{name}_q" in q_formats else q_formats['default_q']
	varnames = engine.__init__.__code__.co_varnames
	if 'limit' in varnames and 'count' in varnames:
		attr = engine(q, limit, count)
	elif 'limit' in varnames:
		attr = engine(q, limit)
	else:
		attr = engine(q)

	attr.run_crawl()
	LINKS += attr.links
	PAGES += attr.pages

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	engine = self.options['engine'].split(',')
	output = {'links': [], 'profiles': [], 'tags': []}
	q_formats = {
		'default_q': f"site:www.stackoverflow.com {query}",
		'millionshort_q': f'site:www.stackoverflow.com "{query}"'
	}

	self.thread(search, self.options['thread'], engine, query, q_formats, limit, count, meta['sources'])
	links = list(self.reglib().filter(r'https?://(www\.)?stackoverflow\.com', list(set(LINKS))))
	for link in links:
		first_type = re.search(r'stackoverflow\.com/[Qq]uestions/[\d]*/([\w\d\-_]+)/?', link)
		if first_type:
			title = first_type.group(1).replace('-', ' ').title()
			title = self.urlib(title).unquote.title()
		else:
			title = 'Matching Result [Without Title]'
		output['links'].append([link, title])

	for link in links:
		link = re.sub(r'https?://(www\.)stackoverflow\.com/users/', '', link)
		if re.search(r'^[\w\d_\-\/]+$', link):
			link = link.rsplit('/')
			output['profiles'].append(link[0])

	for link in links:
		if '/tags/' in link:
			link = re.sub(r'https?://(www\.)?stackoverflow\.com/tags/', '', link)
			if re.search(r'^[\w\d_\-]+$', link):
				output['tags'].append(f"#{link}")
	self.save_gather(output, 'search/stackoverflow', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)
	for i in range(len(output['links'])):
		self.output(f"{output['links'][i][1]}")
		self.output(f"\t{output['links'][i][0]}", 'G')
	output.pop('links')
	self.alert_results(output)
