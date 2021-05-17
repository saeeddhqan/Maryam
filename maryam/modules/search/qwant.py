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
	'name': 'Qwant Search',
	'author': 'Saeed',
	'version': '0.2',
	'description': 'Search your query in the qwant.com and show the results(without limit).',
	'sources': ('qwant',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('method', 'webpages', False, 'Qwant methods("webpages",\
		 "images", "news", "videos"). default=None', '-m', 'store', str),
		('limit', 2, False, 'Search limit(number of pages, default=2)', '-l', 'store', int),
	),
	'examples': ('qwant -q <QUERY>', 'qwant -q <QUERY> -m images -l 3')
}

def module_api(self):
	query = self.options['query']
	run = self.qwant(query, self.options['limit'])
	method = self.options['method'].lower()
	if method not in ('webpages', 'images', 'news', 'videos'):
		method = 'webpages'

	run.run_crawl(method)
	output = {'links': run.links_with_title}
	self.save_gather(output, 'search/qwant', query, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)
	for item in output['links']:
		title, link = item[0], item[1]
		self.output(title)
		self.output(f"\t{link}", 'G')
