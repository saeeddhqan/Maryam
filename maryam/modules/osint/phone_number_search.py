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
	'name': 'Phone Number Search',
	'author': 'Kaushik',
	'version': '0.1',
	'description': 'A Search Engine for Phone Number Enumeration.',
	'sources': ('numverify'),
	'options': (
			('number', None, True, 'Phone number (Must include area code)', '-n', 'store', str),
	),
	'examples': ('phone_number_search -n 911234567890')
}

def module_api(self):
	num = self.options['number']
	run = self.numverify(num)
	run.run_crawl()
	output = run.json
	self.save_gather(output, 'osint/phone_number_search', num, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)
	if output['valid']:
		self.alert_results(output)
	else:
		self.error('Invalid Number!', 'phone_number_search', 'module_run')
		self.error("Number must be of the form '+{area code}{ten digit number}'", 'phone_number_search', 'module_run')
