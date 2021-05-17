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
	'name': 'Facebook Search',
	'author': 'Saeed',
	'version': '0.1',
	'description': 'Search your query in the facebook.com and show the results.',
	'sources': ('google', 'carrot2', 'bing', 'yahoo', 'millionshort', 'qwant', 'duckduckgo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
		('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store', str),
	),
	'examples': ('facebook -q <QUERY> -l 15 --output',)
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
	output = {'links': [], 'people': [], 'groups': [], 'hashtags': []}
	q_formats = {
		'default_q': f"site:facebook.com {query}",
		'millionshort_q': f'site:facebook.com "{query}"',
		'qwant_q': f'site:facebook.com {query}'
	}

	self.thread(search, self.options['thread'], engine, query, q_formats, limit, count, meta['sources'])

	usernames = self.page_parse(PAGES).get_networks
	for _id in list(set(usernames.get('Facebook'))):
		_id = _id[_id.find('/')+1:]
		if _id not in output['people']:
			output['people'].append(_id)

	links = list(self.reglib().filter(r"https?://([A-z\-\.]+\.)?facebook\.com/", list(set(LINKS))))
	for link in filter(lambda x: '/hashtag/' in x, links):
		tag = re.sub(r"https?://([A-z\-\.]+\.)?facebook\.com/hashtag/", '', link).replace('/', '')
		if re.search(r'^[\w\d_\-\/]+$', tag):
			if tag not in output['hashtags']:
				output['hashtags'].append(tag)

	for link in filter(lambda x: '/groups/' in x, links):
		link = re.sub(r"https?://([A-z\-\.]+\.)?facebook\.com/groups/", '', link).replace('/', '')
		if re.search(r'^[\w\d_\-\/]+$', link):
			if link not in output['groups']:
				output['groups'].append(link)

	output['links'] = links
	self.save_gather(output, 'search/facebook', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
