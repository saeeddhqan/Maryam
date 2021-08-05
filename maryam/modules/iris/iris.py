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

import concurrent.futures

meta = {
	'name': 'Iris Meta Search Engine(experiment version)',
	'author': 'Saeed, Kaushik',
	'version': '0.3',
	'description': 'Iris is a built-in meta search engine.',
	'comments': ('It should be note that this is a beta version and has lots of bugs!',),
	'contributors': 'Aman, Dimitris, Divya, Vikas, Kunal',
	'sources': ('google', 'bing', 'duckduckgo', 'millionshort', 'etools'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
	),
	'examples': ('iris -q <QUERY>',)
}

RESULTS = {}
MAPPED = {'google': 100, 'bing': 100, 'duckduckgo': 30, 'millionshort': 10, 'yahoo': 100, 'carrot2': 100, 'searx': 100}

def thread(self, function, query, limit, workers):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=len(workers))
	futures = (threadpool.submit(function, self, x, query, limit) for x in workers)
	for _ in concurrent.futures.as_completed(futures):
		pass

def remove_dups(self, res):
	urls = []
	new = []
	for i in res:
		a = self.urlib(i['a'].lower()).sub_service()
		if a not in urls:
			urls.append(a)
			new.append(i)
	return new

def search(self, name, q, limit):
	global RESULTS
	count = MAPPED[name]
	try:
		engine = getattr(self, name)
		q = q
		varnames = engine.__init__.__code__.co_varnames
		if 'limit' in varnames and 'count' in varnames:
			attr = engine(q, limit, count)
		elif 'limit' in varnames:
			attr = engine(q, limit)
		else:
			attr = engine(q)
		attr.run_crawl()
		RESULTS[name] = attr.results
	except Exception as e:
		print(e)

def module_api(self):
	global RESULTS
	query = self.options['query']
	engines = MAPPED.keys()
	thread(self, search, query, 3, engines)
	simple_merge = self.meta_search_util.simple_merge([RESULTS[x] for x in engines])
	final_results = remove_dups(self, simple_merge)
	output = {'results': final_results}
	self.save_gather(output, 'iris/iris', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
