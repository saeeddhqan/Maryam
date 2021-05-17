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

meta = {
	'name': 'Documentations Search',
	'author': 'Saeed',
	'version': '0.8',
	'description': 'Search in open-sources to find relevant documents. filetypes[pdf,doc,docx,ppt,pptx,xlsx,txt,..].',
	'sources': ('bing', 'google', 'yahoo', 'yandex', 'metacrawler', 'ask',
		'startpage', 'exalead', 'carrot2', 'qwant', 'millionshort', 'duckduckgo', 'gigablast', 'dogpile'),
	'options': (
		('query', None, True, 'Host Name, Company Name, keyword, query, etc', '-q', 'store', str),
		('file', 'pdf', True, 'Filetype [pdf,doc,docx,ppt,pptx,xlsx,txt,..]', '-f', 'store', str),
		('limit', 2, False, 'Search limit(number of pages, default=2)', '-l', 'store', int),
		('count', 50, False, 'number of results per page(min=10)', '-c', 'store', int),
		('site', False, False, 'If this is set, search just limited to the site', '-s', 'store_false', bool),
		('engines', 'exalead,bing,google', True, 'Search engines with comma separator', '-e', 'store', str),
		('thread', 2, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('docs_search -q amazon -f pdf -e google,bing,metacrawler --thread 3',
		'docs_search -q amazon -f pdf -e google,bing,metacrawler -l 3')
}
	
DOCS = []

def search(self, name, q, q_formats, limit, count):
	global DOCS
	try:
		engine = getattr(self, name)
		name = engine.__init__.__name__
		q = q
		varnames = engine.__init__.__code__.co_varnames
		if 'limit' in varnames and 'count' in varnames:
			attr = engine(q, limit, count)
		elif 'limit' in varnames:
			attr = engine(q, limit)
		else:
			attr = engine(q)

		attr.run_crawl()
		DOCS += attr.docs
	except Exception as e:
		print(e)

def module_api(self):
	query = self.options['query']
	_type = self.options['file'].lower()
	limit = self.options['limit']
	count = self.options['count']
	engines = self.options['engines'].lower().split(',')
	# Make dork
	if self.options['site']:
		dork = self.urlib(f"filetype:{_type} site:{self.options['site']} {query}").quote
	else:
		dork = f"{query} filetype:{_type}"

	self.thread(search, self.options['thread'], engines, dork, {}, limit, count, meta['sources'])
	output = {_type : list(set(DOCS))}
	self.save_gather(output, 'osint/docs_search', query, \
		[_type], output=self.options['output'])
	return output

def module_run(self):
	self.alert_results(module_api(self))
