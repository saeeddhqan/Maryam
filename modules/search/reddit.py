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
	'name': 'Reddit Search',
	'author': 'Kunal Khandelwal',
	'version': '0.5',
	'description': 'Search your query in the Reddit and show the results.',
	'sources': ('google', 'yahoo', 'bing', 'yippy', 'metacrawler', 'millionshort', 'carrot2', 'qwant'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store'),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store'),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store'),
		('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store'),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store'),
	),
	'examples': ('reddit -q <QUERY> -l 15 --output',)
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
	output = {'posts': [], 'links' : [], 'subreddits' : [], 'usernames': []}
	q_formats = {
		'default_q': f"site:www.reddit.com {query}",
		'yippy_q': f'"www.reddit.com" {query}',
		'millionshort_q': f'site:www.reddit.com "{query}"',
		'qwant_q': f'site:www.reddit.com {query}'
	}
	
	thread(search, self, self.options['thread'], engines, query, q_formats, limit, count)
	
	usernames = []
	subreddits = []
	links = list(set(LINKS))
	links = list(self.reglib().filter(r"https?://(www\.)?reddit\.com/", links))
	for link in self.reglib().filter(r"https?://(www\.)?reddit\.com/user/", links):
		link = re.sub(r"https?://(www\.)?reddit\.com/user/", '', link)
		if re.search(r'^[\w\d_\-\/]+$', link):
			link = link.rsplit('/')
			if link[0] not in usernames:
				usernames.append(link[0])

	for link in links:
		if re.search(r"reddit\.com/r/", link) and "/about/" not in link:
			post_url = re.sub(r"https?://(www\.)?reddit\.com/r/", '', link)
			post_url = post_url.rsplit('/')
			subreddit = post_url[0]
			try:
				post = post_url[3]
			except Exception as e:
				continue

			post = post.replace('_', ' ')
			post = self.urlib(post).unquote
			output['posts'].append(post.title())
			subreddits.append(f'r/{subreddit}')
			output['links'].append(link)

	output['usernames'] = list(set(usernames))
	output['subreddits'] = list(set(subreddits))
	self.save_gather(output,'search/reddit', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))