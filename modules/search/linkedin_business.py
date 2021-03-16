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

import concurrent.futures

meta = {
	'name': 'Business Linkedin Search',
	'author': 'Dimitrios Papageorgiou',
	'version': '0.1',
	'description': 'Search your query in the Business Linkedin and show the results.',
	'sources': ('google', 'yahoo', 'bing', 'yippy', 'metacrawler', 'millionshort', 'carrot2', 'qwant'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store'),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store'),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
		('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
	),
	'examples': ('business_linkedin -q <QUERY> -e carrot2,bing,qwant -c 50 --output',)
}

LINKS = []

def set_data(urls):
	for url in urls:
		LINKS.append(url)

def thread(function, self, thread_count, engines, q, q_formats, limit, count):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
	futures = (threadpool.submit(
		function, self, name, q, q_formats, limit, count) for name in engines if name in meta['sources'])
	for _ in concurrent.futures.as_completed(futures):
		pass

def search(self, name, q, q_formats, limit, count):
	global LINKS
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
	set_data(attr.links)

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	engines = self.options['engine'].split(',')
	output = {'links' : []}
	q_formats = {
		'default_q': f"site:business.linkedin.com {query}",
		'meta_q': f'"business.linkedin.com" {query}'
	}

	thread(search, self, self.options['thread'], engines, query, q_formats, limit, count)
	links = self.reglib().filter(r"https?:\/\/business\.linkedin\.com/", LINKS)
	output['links'] = list(set(links))

	self.save_gather(output, 'search/business_linkedin', query, output=self.options.get('output'))
	return output 


def module_run(self):
	self.alert_results(module_api(self))
