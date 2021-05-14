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

from maryam.core.basedir import BASEDIR

meta = {
	'name': 'Username Search',
	'author': 'Aman Singh',
	'version': '0.5',
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
	futures = (threadpool.submit(check, self, data[site]['url'].format(self.urlib(query).quote_plus.replace('.', '%2E')), site, data) for site in data)
	for results in concurrent.futures.as_completed(futures):
		print(f"Found {len(OUTPUT['links'])} accounts" , end='\r')
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
		elif str(req.status_code)[0] == '2' or str(req.status_code)[0] == '3':
			OUTPUT['links'][site] = {'url': url, 'rank': data[site]['rank']}

def module_api(self):
	query = self.options['query']
	filepath = os.path.join(BASEDIR,
				'data',
				'username_checker.json')
	with open(filepath) as handle:
		data = json.load(handle)
	thread(self, data, query,self.options['thread'])
	output = OUTPUT
	self.save_gather(
		output,
		'osint/username_search',
		query,
		output=self.options.get('output')
	)
	output['links'] = sorted(
		list(output['links'].items()), key=lambda x: int(x[1]['rank'])
	)
	return output

def module_run(self):
	output = module_api(self)

	sites = [(name, meta['url']) for name, meta in output['links']]

	self.alert("Accounts Found (sorted by site's rank)")
	self.table(sites , header=['Site', 'Account'], linear=True, sep='_')

def refresh_username_checker_siteranks():
	"""
	Function which refreshes the `rank` properity in `username_checker.json`.
	This method should only be called manually.
	To fetch data you need an API key. To obtain it, register at:
	https://www.domcop.com/openpagerank/
	"""
	import requests
	from urllib.parse import urlparse

	API_KEY = input('Please input your OpenSiteRank API key: ')

	def getRank(url):
		header = {'API-OPR': API_KEY}
		req_url = f"https://openpagerank.com/api/v1.0/getPageRank?domains[]={url}"
		r = requests.get(req_url, headers=header)
		result = json.loads(r.text)	
		return result

	data = dict()

	filepath = os.path.join(BASEDIR,
				'data',
				'username_checker.json')

	with open(filepath, 'r') as f:
		data = json.load(f) 

	for site in data:
		domain = urlparse(data[site]['url']).netloc.replace('{}.', '')
		rank = getRank(domain)
		if rank['status_code'] != 200:
			print('\nERROR:\n', rank)
		else:
			data[site]['rank'] = rank['response'][0]['rank']

	with open(filepath, 'w') as f:
		f.write(json.dumps(data))

