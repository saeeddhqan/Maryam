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
	'name': 'CRT Search',
	'author': 'Saeed',
	'version': '0.2',
	'description': 'Search your query in the crt.sh and show the results.',
	'sources': ('crt',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
	),
	'examples': ('crt -q <QUERY>',)
}

def module_api(self):
	query = self.options['query']
	run = self.crt(query)
	run.run_crawl()
	output = run.json_page
	self.save_gather({'certificates': output}, 'search/crt', query, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)
	items = []
	for itm in output:
		i_d = f"https://crt.sh/?caid={itm.get('id')}"
		entry_timestamp = itm.get('entry_timestamp').split('T')[0]
		not_before = itm.get('not_before').split('T')[0]
		not_after = itm.get('not_after').split('T')[0]
		nvalue = itm.get('name_value')
		issuer = f"https://crt.sh/?caid={itm.get('issuer_ca_id')}"
		if '\n' in nvalue:
			for line in nvalue.split('\n'):
				items.append((i_d, entry_timestamp, not_before, not_after, line, issuer))
			continue
		items.append((i_d, entry_timestamp, not_before, not_after, nvalue, issuer))
	self.table(items, header=['crt.sh ID', 'Logged at', 'Not Before', 'Not After', 'Maching Identities', 'Issuer Name'], linear=True, sep='_')
