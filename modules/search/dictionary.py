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
        'name': 'Dictionary',
        'author': 'Kaushik',
        'version': '0.1',
        'description': 'This module uses an unofficial google dictionary api to fetch \
			definitions of query.',
        'sources': ('dictionary',),
        'options': (
                ('query', None, True, 'Query to search', '-q', 'store', str),
        ),
        'examples': ('dictionary -q <QUERY>',)
}

def module_api(self):
	query = self.options['query']
	run = self.dictionary(query)
	run.run_crawl()
	output = {'results': []}
	definitions = run.definitions

	for item in definitions:
		output['results'].append(item)

	self.save_gather(output, 'search/dictionary', query, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)['results']
	for item in output:
		print()
		self.output(f"As {item['partOfSpeech']}")
		self.output(item['definition'])
