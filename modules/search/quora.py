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
	'name': 'Quora Search',
	'author': 'Aman Rawat',
	'version': '0.2',
	'description': 'Search your query in the quora.com and show the results.',
	'sources': ('google', 'yahoo', 'bing', 'metacrawler', 'millionshort', 'carrot2', 'qwant', 'duckduckgo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store', int),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
		('engine', 'bing', False, 'Engine names for search(default=bing)', '-e', 'store', str),
	),
	'examples': ('quora -q <QUERY> -l 15 --output',)
}

LINKS = []

def search(self, name, q, q_formats, limit, count):
	global LINKS
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
	if name == 'google':
		LINKS += [(x['a'], x['t']) for x in attr.results_original]
	LINKS += attr.links

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	engines = self.options['engine'].split(',')
	output = {'links': [], 'usernames': []}
	q_formats = {
		'default_q': f"site:www.quora.com {query}",
		'millionshort_q': f'site:www.quora.com "{query}"',
		'qwant_q': f'site:www.quora.com {query}'
	}

	self.thread(search, self.options['thread'], engines, query, q_formats, limit, count, meta['sources'])

	links = list(set(LINKS))
	for link in self.reglib().filter(r"https?://(www\.)?quora\.com/profile/", links):
		if link not in output['usernames']:
			output['usernames'].append(link)

	for link in links:
		if re.search(r"https?://(www\.)?quora\.com", link) and '/profile' not in link:
			title = re.sub(r"https?://(www\.)?quora\.com/", '', link)
			title = title.replace('-', ' ')
			title = self.urlib(title).unquote.split('?')[0]
			output['links'].append([link, title])

	self.save_gather(output, 'search/quora', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)
	self.alert('usernames')
	for user in output['usernames']:
		self.output(f"\t{user}", 'G')
	self.alert('links')
	for item in output['links']:
		title, link = item[1], item[0]
		self.output(title)
		self.output(f"\t{link}", 'G')
		print('')
