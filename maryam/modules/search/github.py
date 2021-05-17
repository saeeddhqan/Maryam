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
	'name': 'GitHub Search',
	'author': 'Aman Singh',
	'version': '1.0',
	'description': 'Search your query in the GitHub and show the results.',
	'sources': ('google', 'carrot2', 'bing', 'yahoo', 'millionshort', 'qwant', 'duckduckgo', 'github'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
		('engine', 'google,github', False, 'Engine names for search(default=google, github)', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
    'examples': ('github -q <QUERY> -l 15 -e carrot2,bing,qwant --output',)
}

LINKS = []
PAGES = ''
USERS = []
REPO = []
EMAILS = []

def search(self, name, q, q_formats, limit, count):
	global PAGES, LINKS, USERS, REPO, EMAILS
	engine = getattr(self, name)
	eng = name
	q = q_formats[f"{name}"] if f"{name}" in q_formats else q_formats['default']
	varnames = engine.__init__.__code__.co_varnames
	if 'limit' in varnames and 'count' in varnames:
		attr = engine(q, limit, count)
	elif 'limit' in varnames:
		attr = engine(q, limit)
	else:
		attr = engine(q)
	if eng == 'github':
		run = self.github(q)
		run.run_crawl()
		USERS += run.users
		REPO += run.repositories
		EMAILS = run.emails
	else:
		attr.run_crawl()
		LINKS += attr.links
		PAGES += attr.pages

def module_api(self):
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	engines = self.options['engine'].split(',')
	output = {'repositories': [], 'blogs': [], 'usernames': [], 'emails': set()}
	q_formats = {
		'default': f"site:github.com {query}",
		'millionshort': f'site:github.com "{query}"',
		'qwant': f'site:github.com {query}',
		'github': f'{query}'
	}

	self.thread(search, self.options['thread'], engines, query, q_formats, limit, count, meta['sources'])

	explore = self.page_parse(PAGES).get_networks
	output['blogs'] = list(set(explore['Github site']))
	bactery = ['marketplace', 'pulls', 'explore', 'issues',\
				'notifications', 'account', 'settings', 'login',\
				'about', 'pricing', 'site']
	for user in set(explore['Github'][1:]):
		user = user.split('/')[1]
		if user not in bactery:
			output['usernames'].append(user)
	for user in USERS[1:]:
		user = user.split('/')[1]
		output['usernames'].append(user)

	for link in self.reglib().filter(r"https://(www\.)?github\.com/[\w-]{1,39}/[\w\-\.]+", list(set(LINKS))):
		repo = re.search(r"(https://(www\.)?github\.com/([\w-]{1,39})/[\w\-\.]+)", link)
		if repo.group(3) not in bactery:
			repo = repo.group(0)
			if repo not in output['repositories']:
				output['repositories'].append(repo)
	for link in REPO:
		output['repositories'].append(link)
	
	output['emails'] = EMAILS
	self.save_gather(output,
	 'search/github', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
