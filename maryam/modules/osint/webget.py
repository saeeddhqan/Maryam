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
	'name': 'Webget',
	'author': 'Rishabh Jain',
	'version': '0.1',
	'description': 'Download the files form the web by url or request response',
	'sources': ('google', 'bing', 'yahoo', 'searx', 'peekier', 'gigablast', 'zapmeta', 'millionshort'),
	'comments': (
		"""example: -q 'http://www.africau.edu/images/default/sample.pdf' -g pdf""",
	),
	'options': (
		('query', None, True, 'url to down load', '-q', 'store', str),
		('getType', None, False, 'get-type of the file to download specified file endpoints (default ALL files types)', '-g', 'store', str),
	),
	'examples': ('webget -q <url> -g <type>',)
}

import os

def module_api(self) :
	query = self.options['query']
	getType = self.options['getType'] or ''
	run = self.downloader.get(url=query, type=[getType] if getType else [] )
	return (os.path.basename(run) if run else None)
    
def module_run(self):
	results = module_api(self)
	if results:
		self.alert_results(results)