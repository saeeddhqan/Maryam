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
        'name': 'SanctionSearch',
        'author': 'Kaushik',
        'version': '0.1',
        'description': 'SanctionSearch is an international list of blacklisted, dangerous\
		personnel and entities.',
        'sources': ('sanctionsearch',),
        'options': (
		('query', None, False, 'Name to search', '-q', 'store', str),
		('id', None, False, 'Id to search', '-i', 'store', int),
		('limit', 15, False, 'Max result count (default=15)', '-l', 'store', int),
        ),
        'examples': ('sanctionsearch -q <QUERY> -l 20',
		'sanctionsearch -i <ID>')
}

NAMESEARCH = False

def module_api(self):
	global NAMESEARCH

	query = self.options['query']
	limit = self.options['limit']
	_id = self.options['id']

	if query is None and _id is None:
		return {}
	elif query is not None and _id is not None:
		_id = None
	elif query is not None:
		NAMESEARCH = True
	
	run = self.sanctionsearch(query=query, id=_id, limit=limit)

	if NAMESEARCH:
		output_param = query
		run.name_crawl()
		output = {'results': []}
		data = run.data
		for item in data:
			output['results'].append(item)
	else:
		output_param = _id
		run.id_crawl()
		output = run.data

	self.save_gather(output, 'search/sanctionsearch', output_param, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)
	if NAMESEARCH:
		output = output['results']
		for name in output:
			print()
			self.output(name['name'])
			if len(name['address'].strip()) > 0:
				self.output(name['address'])
			self.output(name['link'])
	else:
		if output is not None:
			self.alert_results(output)
