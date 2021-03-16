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
	'name': 'Twitter Search',
	'author': 'Saeeddqn',
	'version': '0.5',
	'description': 'Search your query in the twitter.com and show the results.',
	'sources': ('google', 'carrot2', 'bing', 'yippy', 'yahoo', 'millionshort', 'qwant', 'duckduckgo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store'),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
		('count', 50, False, 'The number of results per page(min=10, max=100,\
			default=50)', '-c', 'store'),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
		('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
	),
	'examples': ('twitter -q <QUERY> -l 15 --output',)
}

LINKS = []
PAGES = ''

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
	global PAGES
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
	PAGES += attr.pages

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	engines = self.options['engine'].split(',')

	output = {'links': [], 'people': [], 'hashtags': []}
	q_formats = {
		'default_q': f"site:twitter.com {query}",
		'millionshort_q': f'site:twitter.com "{query}"',
		'yippy_q': f"twitter.com {query}"
	}

	thread(search, self, self.options['thread'], engines, query, q_formats, limit, count)

	usernames = self.page_parse(PAGES).get_networks
	for _id in list(set(usernames.get('Twitter'))):
		if isinstance(_id, (tuple, list)):
			_id = _id[0]
			_id = f"@{_id[_id.find('/') + 1:]}"
		else:
			_id = f"@{_id[_id.find('/') + 1:]}"
		output['people'].append(_id)

	links = list(set(LINKS))
	links = list(self.reglib().filter(lambda x: 'twitter.com' in x and '.twitter.com' not in x, links))
	for link in self.reglib().filter(lambda x: '/hashtag/' in x, links):
		link = re.sub(r'https?://(www\.)?twitter.com/hashtag/', '', link)
		if re.search(r"^[\w\d_\-]+$", link):
			output['hashtags'].append(link)

	output['links'] = links

	self.save_gather(output,
		'search/twitter', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))