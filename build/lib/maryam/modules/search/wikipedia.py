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
	'name': 'Wikipedia Search',
	'author': 'Tarunesh Kumar',
	'version': '0.3',
	'description': 'Search your query in the Wikipedia and show the results.',
	'sources': ('wikipedia',),
	'options': (
		('query', None, False, 'Query string or wiki page id(e.g, 64959383)', '-q', 'store', str),
		('count', 50, False, 'Number of links per page(min=10, max=100, default=50)', '-c', 'store', int),
	),
	'examples': ('wikipedia -q 64959383',)
}

def module_api(self):
	query = self.options['query']
	count = self.options['count']
	wiki = self.wikipedia(query, count)
	target = ''
	output = {'titles': [], 'links': [], 'page': {}}
	if query.isnumeric() and len(query) > 3:
		output['page'] = wiki.page()
	else:
		wiki.run_crawl()
		links_with_title = wiki.links_with_title
		for link, title, pid in links_with_title:
			output['titles'].append(f"{title}[{pid}]")
		output['links'] = wiki.links

	self.save_gather(output, 'search/wikipedia', query, output=self.options.get('output'))	
	return output

def module_run(self):
	output = module_api(self)
	if output['page'] == {}:
		self.alert('links')
		for i in range(len(output['titles'])):
			self.output(output['titles'][i])
			self.output(f"\t{output['links'][i]}", 'G')
		return
	page = {**output['page']}
	target = page.pop('title', self.options['query'])
	if 'extract' not in page:
		self.output('Not found')
		return
	description = page.pop('extract')
	header = ['Key', 'Value']
	self.table(page.items(), header, title=target)
	self.heading('Description')
	self.output(self.textwrapping('\t', description), prep='\t')
