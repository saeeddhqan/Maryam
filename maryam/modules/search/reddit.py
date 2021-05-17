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
	'version': '1.0',
	'description': 'Search your query in the Reddit and show the results.',
	'sources': ('google', 'yahoo', 'bing', 'metacrawler', 'millionshort', 'carrot2', 'duckduckgo', 'qwant', 'reddit_pushshift'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
		('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
		('search-type', 'posts', False, 'Type of search i.e. posts or comments(default=posts)', '-s', 'store', str),
		('username', '', False, 'Search data of a particular username', '-u', 'store', str),
		('subreddit', '', False, 'Search data in a particular subreddit', '-r', 'store', str),
		('before', '', False, 'Search data before this date(format=d/m/y H:M:S) i.e. 7/6/21 12:0:0', '-b', 'store', str),
		('after', '', False, 'Search data after this date(format=d/m/y H:M:S) i.e. 7/6/21 12:0:0', '-a', 'store', str),
		('score', '', False, 'Score of the data to search i.e. >1 or <2 etc.', '-o', 'store', str),
	),
	'examples': ('reddit -q <QUERY> -l 15 --output',)
}

LINKS = []
PAGES = ''
USERNAMES = []

def search(self, name, q, q_formats, limit, count, search_type, username, subreddit, before, after, score):
	global PAGES,LINKS,USERNAMES
	engine = getattr(self, name)
	q = q_formats[f"{name}_q"] if f"{name}_q" in q_formats else q_formats['default_q']
	varnames = engine.__init__.__code__.co_varnames
	if 'limit' in varnames and 'count' in varnames:
		attr = engine(q, limit, count)
	elif 'limit' in varnames:
		attr = engine(q, limit)
	elif name == 'reddit_pushshift':
		attr = engine(q, count, search_type, username, subreddit, before, after, score)	
	else:
		attr = engine(q)
	
	# Some engines like reddit_pushshift return direct usernames so to avoid errors in other engines, check first
	attr.run_crawl()
	LINKS += attr.links if hasattr(attr, 'links') else []
	PAGES += attr.pages if hasattr(attr, 'pages') else ''
	USERNAMES += attr.usernames if hasattr(attr, 'usernames') else []


def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	engine = self.options['engine'].split(',')
	search_type = self.options['search_type']
	username = self.options['username']
	subreddit = self.options['subreddit']
	before = self.options['before']
	after = self.options['after']
	score = self.options['score']

	output = {'links': [], 'usernames': []}
	q_formats = {
		'default_q': f"site:www.reddit.com {query}",
		'millionshort_q': f'site:www.reddit.com "{query}"',
		'qwant_q': f'site:www.reddit.com {query}',
		'reddit_pushshift_q': query
	}
	
	self.thread(search, self.options['thread'], engine, query, q_formats, limit, count, search_type, username, subreddit, before, after, score, meta['sources'])

	links = list(self.reglib().filter(r"https?://(www\.)?reddit\.com/", list(set(LINKS))))

	for i in USERNAMES: # For classes that return direct usernames
		output['usernames'].append(i)

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
