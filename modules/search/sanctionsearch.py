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
        'name': 'SanctionSearch',
        'author': 'Kaushik',
        'version': '0.1',
        'description': 'SanctionSearch is an international list of blacklisted, dangerous\
		personnel and entities.',
        'sources': ('sanctionsearch'),
        'options': (
		('name', None, False, 'name to search', '-n', 'store', str),
		('id', None, False, 'id to search', '-i', 'store', int),
		('limit', 15, False, 'Max result count (default=15)', '-l', 'store', int),
        ),
        'examples': ("sanctionsearch -n <QUERY> -l 20 ",
		"sanctionsearch -i <ID>")
}

NAMESEARCH = False

def module_api(self):
	global NAMESEARCH

	name = self.options['name']
	limit = self.options['limit']
	id = self.options['id']

	if name is None and id is None:
		self.error('Either name or id is required')
		return
	elif name is not None and id is not None:
		self.error('Only specify either name or id not both')
		return
	elif name is not None:
		NAMESEARCH = True
	
	run = self.sanctionsearch(name=name, id=id, limit=limit)

	if NAMESEARCH:
		output_param = name
		run.name_crawl()
		output = {'results': []}
		links = run.data

		for item in links:
			output['results'].append(item)


	else:
		output_param = id
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
			if len(name['address'].strip())>0:
				self.output(name['address'])
			self.output(name['link'])
	else:
		output = module_api(self)
		if output is not None:
			self.alert_results(output)
