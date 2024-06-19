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
	'name': 'Image Search',
	'author': 'Saeed',
	'version': '0.1',
	'description': 'Search in open-sources to find images.',
	'sources': ('bing', 'google'),
	'options': (
		('query', None, True, 'Query, host Name, company Name, keyword, , etc', '-q', 'store', str),
		('engines', 'google', True, 'Search engines with comma separator', '-e', 'store', str),
		('thread', 3, False, 'The number of engine that run per round(default=2)', '-t', 'store', int),
	),
	'examples': ('image_search -q amazon -e google,bing,qwant',)
}
	
IMGS = []
def remove_dups(self):
	urls = []
	new = []
	for i in IMGS:
		a = self.urlib(i['i'].lower()).sub_service()
		if a not in urls:
			urls.append(a)
			new.append(i)
	return new

def search(self, name, q):
	global IMGS
	try:
		engine = getattr(self, name + '_images')
		q = q
		varnames = engine.__init__.__code__.co_varnames
		attr = engine(q)

		attr.run_crawl()
		IMGS += attr.results
	except Exception as e:
		print(e)

def module_api(self):
	query = self.options['query']
	engines = self.options['engines'].lower().split(',')

	self.thread(search, self.options['thread'], engines, query, meta['sources'])
	INGS = remove_dups(self)
	output = {'results' : IMGS}
	self.save_gather(output, 'osint/image_search', query, output=self.options['output'])
	return output

def module_run(self):
	for i in module_api(self)['results']:
		self.output(i['a'])
		self.output(i['i'])
		self.output(i['t'])
		self.output(i['d'])
		print()
