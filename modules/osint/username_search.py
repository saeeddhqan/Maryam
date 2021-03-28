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

import os
import json
import concurrent.futures
import urllib
from os.path import dirname as up

meta = {
	'name': 'Username Search',
	'author': 'Aman Singh',
	'version': '0.1',
	'description': 'Search your query across 100+ social networks and show the results.',
	'sources': ('https://github.com/sherlock-project/sherlock',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('thread', 64, False, 'The number of sites that are being checked per round(default=8)', '-t', 'store', int),
	),
	'examples': ('username_search -q <QUERY> --output',)
}

OUTPUT = {'links': {}}

def thread(self, data, query,thread_count):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
	futures = (threadpool.submit(check, self, data[site]['url'].format(urllib.parse.quote_plus(query).replace('.','%2E')), site, data) for site in data)
	for results in concurrent.futures.as_completed(futures):
		print(f"Found {len(OUTPUT['links'])} accounts" , end= '\r')
	print('\n')


def check(self, url, site, data):
	global OUTPUT
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		req = self.request(url, headers=headers, timeout=20)
	except Exception as e:
		return
	else:
		if str(req.status_code) == data[site]['status']:
			for error in data[site]['error']:
				if error in req.text :
					return
		elif(str(req.status_code)[0] == '2' or str(req.status_code)[0] == '3'):
			OUTPUT['links'][site] = url

def module_api(self):
	query = self.options['query']
	project_root = up(up(up(__file__)))
	filepath = os.path.join(project_root,
				'data',
				'username_checker.json')
	with open(filepath) as handle:
		data = json.load(handle)
	thread(self, data, query,self.options['thread'])
	output = OUTPUT

	self.save_gather(output, 'osint/username_search', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)
	sites = [(link, output['links'][link]) for link in output['links']]

	self.alert('Accounts Found')
	self.table(sites , header=['Site', 'Account'], linear=True, sep='_')
