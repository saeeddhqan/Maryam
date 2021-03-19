import re
import os
import json

meta = {
	'name': 'Username Search',
	'author': 'Aman Singh',
	'version': '0.1',
	'description': 'Search your query across 100+ social networks and show the results.',
	'sources': ('google', 'carrot2', 'bing', 'yippy', 'yahoo', 'millionshort', 'qwant', 'duckduckgo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
		('engine', 'google,carrot2', False, 'Engine names for search(default=google)', '-e', 'store', str),
	),
    'examples': ('username_checker -q <QUERY> -l 15 --output',)
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
	output = {'sites': []}

	filepath = os.path.join(os.getcwd(), 'data','username_checker.json')
	file = open(filepath)
	data = json.loads(file.read())

	for site in data:

		q_formats = {
			'default_q': data[site]['url'].format(query)
		}

		self.thread(search, self.options['thread'], engine, query, q_formats, limit, count, meta['sources'])
	output['site'] = list(set(LINKS))
	self.save_gather(output, 'search/username_checker', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
