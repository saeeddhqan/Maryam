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
	'name': 'Instagram Search',
	'author': 'Aman Singh',
	'version': '0.2',
	'description': 'Search your query in the Instagram and show the results.',
	'sources': ('google', 'carrot2', 'bing', 'yippy', 'yahoo', 'millionshort', 'qwant', 'duckduckgo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
		('engine', 'google,carrot2', False, 'Engine names for search(default=google)', '-e', 'store', str),
	),
    'examples': ('instagram -q <QUERY> -l 15 --output',)
}

LINKS = []
PAGES = ''

def search(self, name, q, q_formats, limit, count):
	global PAGES,LINKS
	engine = getattr(self, name)
	name = engine.__init__.__name__
	q = f"{name}_q" if f"{name}_q" in q_formats else q_formats['default_q']
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
	output = {'people': [], 'posts': [], 'hashtags': []}
	q_formats = {
		'google_q': f"site:www.instagram.com inurl:{query}",
		'default_q': f"site:www.instagram.com {query}",
		'yippy_q': f"www.instagram.com {query}"
	}

	self.thread(search, self.options['thread'], engine, query, q_formats, limit, count, meta['sources'])

	usernames = self.page_parse(PAGES).get_networks
	for _id in list(set(usernames.get('Instagram'))):
		if _id[-2:] == "/p" or _id[-8:] == '/explore':
			continue
		_id = f"{_id[_id.find('/')+1:]}"

		if _id not in output['people']:
			output['people'].append(_id)

	links = list(self.reglib().filter(r"https?://(www\.)?instagram\.com/", list(set(LINKS))))
	for link in self.reglib().filter(lambda x: '/explore/tags/' in x, links):
		tag = re.sub(r'https?://(www\.)?instagram\.com/explore/tags/', '', link)
		if re.search(r'^[\w\d_\-\/]+$', tag):
			tag = tag.rsplit('/')
			output['hashtags'].append(tag[0])

	self.alert('posts')
	for link in self.reglib().filter(r'https?://(www\.)?instagram\.com/p/[\w_\-0-9]+/', links):
		output['posts'].append(link)

	self.save_gather(output,
					 'search/instagram', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
