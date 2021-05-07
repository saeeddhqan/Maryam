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
	'name': 'Reddit Search',
	'author': 'Kunal Khandelwal',
	'version': '0.5',
	'description': 'Search your query in the Reddit and show the results.',
	'sources': ('google', 'yahoo', 'bing', 'yippy', 'metacrawler', 'millionshort', 'carrot2', 'qwant'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
		('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('reddit -q <QUERY> -l 15 --output',)
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
	output = {'links': [], 'usernames': []}
	q_formats = {
		'default_q': f"site:www.reddit.com {query}",
		'yippy_q': f'"www.reddit.com" {query}',
		'millionshort_q': f'site:www.reddit.com "{query}"',
		'qwant_q': f'site:www.reddit.com {query}'
	}

	self.thread(search, self.options['thread'], engine, query, q_formats, limit, count, meta['sources'])

	links = list(self.reglib().filter(r"https?://(www\.)?reddit\.com/", list(set(LINKS))))

	usernames = self.page_parse(PAGES).get_networks
	for user in list(set(usernames.get('Reddit'))):
		user = user[(user.rfind('/'))+1:]
		if user not in output['usernames']:
			output['usernames'].append(user)
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
			output['links'].append([link, f"{post.title()} => r/{subreddit}"])

	self.save_gather(output,
					 'search/reddit', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)
	self.alert('usernames')
	for user in output['usernames']:
		self.output(f"\t{user}", 'G')
	self.alert('links')
	for item in output['links']:
		link,title = item[0],item[1]
		self.output(f"\t{title}")
		self.output(f"\t\t{link}", 'G')
