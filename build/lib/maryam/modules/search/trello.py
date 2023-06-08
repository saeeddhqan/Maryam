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
	'name': 'Trello Search',
	'author': 'Vikas Kundu',
	'version': '0.5',
	'description': 'Search public trello boards for data and show the results.',
	'sources': ('google', 'carrot2', 'bing', 'yahoo', 'millionshort', 'qwant', 'duckduckgo'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store', int),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
		('engine', 'google', False, 'Engine names for search(default=google)', '-e', 'store', str),
	),
    'examples': ('trello -q <QUERY> -l 15 --output',)
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
	engines = self.options['engine'].split(',')
	output = {'links': [], 'usernames': [], 'handles': []}
	q_formats = {
		'default_q': f"site:trello.com {query}",
		'millionshort_q': f'site:trello.com "{query}"',
		'qwant_q': f'site:trello.com {query}'
	}

	self.thread(search, self.options['thread'], engines, query, q_formats, limit, count, meta['sources'])
	
	output['links'] = list(self.reglib().filter(r"https?://([\w\-\.]+\.)?trello\.com/", list(set(LINKS))))
	output['handles'] = [ i for i in set(re.findall(r"@[\w]+", PAGES)) if i not in ['@keyframes', '@media','@font']  ]

	output['usernames'] = [ i.replace('(','@') for i in set(re.findall(r"\([\w]{3,}\)", PAGES)) if query in i  ]
	output['usernames'] = [ i.replace(')','') for i in output['usernames'] ]

	#using re directly instead of reglib().filter because when PAGES is passed a list,
	#it becomes useless for searching trello usernames. See: https://ibb.co/Rz182Bj
	
	self.save_gather(output, 'search/trello', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
