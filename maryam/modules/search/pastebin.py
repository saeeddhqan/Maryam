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
	'name': 'Pastebin Search',
	'author': 'Divya Goswami',
	'version': '1.0',
	'description': 'Search your query in the pastebin.com and show the results as paste links.',
	'sources': ('pastebin',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 50, False, 'Number of results per page(min=10, max=100, default=50)', '-c', 'store', int),
		('thread', 3, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
		('engine', 'pastebin', False, 'Engine names for search', '-e', 'store', str),
	),
	'examples': ('pastebin -q passwords -l 15 --output',)
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
	output = {'pastes': []}
	q_formats = {
		'default_q': f"{query}"
	}
	self.thread(search, self.options['thread'], engine, query, q_formats, limit, count, meta['sources'])
	links = list(self.reglib().filter(r"https?://pastebin\.com/[\w\d]{2,}", list(set(LINKS))))
	self.verbose('Rearranging paste links [give it a few seconds]...')
	for link in links:
		heading = re.search(r"pastebin\.com/([\w\d]+)", link)
		if heading:
			head_raw = f"https://pastebin.com/raw/{heading.group(1)}"
			try:
				head_req = self.request(url=head_raw).text.splitlines()[0].lstrip()
			except Exception as e:
				self.verbose('Pastebin is missed!')
			else:
				head_title = f"{query} pastes {head_req[:30]}...".ljust(10, ' ')
				title = head_title.title()
		output['pastes'].append([link, title])
	self.save_gather(output, 'search/pastebin', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)
	for i in range(len(output['pastes'])):
		self.output(f"{output['pastes'][i][1]}", 'G')
		self.output(f"\t{output['pastes'][i][0]}", 'N')
	output.pop('pastes')
	self.alert_results(output)
