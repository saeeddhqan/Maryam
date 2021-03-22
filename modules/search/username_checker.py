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
import os
import json
import concurrent.futures

meta = {
	'name': 'Username Search',
	'author': 'Aman Singh',
	'version': '0.1',
	'description': 'Search your query across 100+ social networks and show the results.',
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('thread', 8, False, 'The number of sites that are being checked per round(default=8)', '-t', 'store', int),
	),
    'examples': ('username_checker -q <QUERY> --output',)
}

output = {'sites': {}}

def thread(self, data, query,thread_count):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
	futures = (threadpool.submit(check, self, data[site]['url'].format(query), site, data) for site in data)
	for results in concurrent.futures.as_completed(futures):
		print(f"Found {len(output['sites'])} accounts" , end= '\r')
	print('\n')


def check(self,url,site, data):
	global output
	try:
		req = self.request(url)
		for error in data[site]['error'] :
			if (error in req.text and str(req.status_code) == data[site]['status']) :
				self.error(f"Not fount on {site}")
				return
		output['sites'][site] = url
	except Exception as e:
		self.error(f"Not fount on {site}")
		return

def module_api(self):
	query = self.options['query']
	filepath = os.path.join(os.getcwd(), 'data','username_checker.json')
	file = open(filepath)
	data = json.loads(file.read())
	thread(self, data, query,self.options['thread'])

	self.save_gather(output, 'search/username_checker', query, output=self.options.get('output'))
	return output

def module_run(self):
	self.alert_results(module_api(self))
