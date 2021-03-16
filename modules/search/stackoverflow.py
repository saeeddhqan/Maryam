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
import concurrent.futures

meta = {
	'name': 'StackOverFlow Search',
	'author': 'Sanjiban Sengupta',
	'version': '0.2',
	'description': 'Search your query in the stackoverflow.com and show the results.',
	'sources': ('google', 'carrot2', 'bing', 'yippy', 'yahoo', 'millionshort', 'qwant', 'duckduckgo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store'),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
		('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store'),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
		('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
	),
	'examples': ('stackoverflow -q "syntax error" -l 15 --output',)
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
	output = {'links': [], 'titles': [], 'profiles': [], 'tags': []}
	q_formats = {
		'default_q': f"site:www.stackoverflow.com {query}",
		'millionshort_q': f'site:www.stackoverflow.com "{query}"'
	}

	thread(search, self, self.options['thread'], engines, query, q_formats, limit, count)

	links = list(set(LINKS))
	links = list(self.reglib().filter(lambda x: 'stackoverflow.com' in x, links))
	
	for link in links:
		first_type = re.search(r'stackoverflow\.com/questions/[\d]+/([\w\d\-_]+)/?', link)
		second_type = re.search(r'stackoverflow\.com/a/[\d+]/?', link)
		if first_type:
			title = first_type.group(1).replace('-', ' ').title()
			title = self.urlib(title).unquote
			output['titles'].append(title)
			output['links'].append(link)
		elif second_type:
			output['titles'].append('No Title')
			output['links'].append(link)

	for link in links:
		link = re.sub(r'https?://(www\.)stackoverflow\.com/users/', '', link)
		if re.search(r'^[\w\d_\-\/]+$', link):
			link = link.rsplit('/')
			output['profiles'].append(link[0])

	for link in links:
		if '/tag/' in link:
			link = re.sub(r'https?://(www\.)?stackoverflow\.com/tags/', '', link)
			if re.search(r'^[\w\d_\-]+$', link):
				output['tags'].append(link)

	self.save_gather(output,'search/stackoverflow', query, output=self.options.get('output'))
	return output


def module_run(self):
	self.alert_results(module_api(self))