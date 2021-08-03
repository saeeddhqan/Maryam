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
	'version': '0.2',
	'description': 'Iris is a meta search engine.',
	'comments': ('It should be note that this is a beta version and has lots of bugs!',),
	'contributors': 'Aman, Dimitris, Divya, Vikas, Kunal',
	'sources': ('google', 'yahoo', 'bing', 'etools', 'metacrawler', 'searx', 'dogpile'),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('engine_count', 3, False, 'Number of engines to use', '-e', 'store', int),
		('limit', 1, False, 'Search limit(number of pages, default=1)', '-l', 'store', int),
		('count', 20, False, 'Number of results per page (default=20)', '-c', 'store', int),
	),
	'examples': ('iris -q <QUERY> -l 15 --output --api',)
}
RESULTS = []
COUNT_CONSENSUS = None
LIMIT_CONSENSUS = None

def thread(self, function, searcher, query, workers):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=workers)
	futures = (threadpool.submit(function, self, searcher, query) for _ in range(workers))
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

def search(self, searcher, q):
	global RESULTS
	engine = searcher._engine_q.pop(0)
	result = searcher.search(
		q,
		engine=engine,
		limit=LIMIT_CONSENSUS[engine] or 1,
		count=COUNT_CONSENSUS[engine]
	)
	RESULTS.append(result)

def module_api(self):
	global COUNT_CONSENSUS, LIMIT_CONSENSUS, RESULTS
	query = self.options['query']
	limit = self.options['limit']
	count = self.options['count']
	workers = self.options['engine_count']
	searcher = self.safe_searcher()

	COUNT_CONSENSUS = self.meta_search_util.compute_count_consensus(searcher._engine_q[:workers], count)
	LIMIT_CONSENSUS = self.meta_search_util.compute_count_consensus(searcher._engine_q[:workers], limit)

	thread(self, search, searcher, query, workers)

	simple_merge = remove_dups(self, self.meta_search_util.simple_merge(RESULTS))
	output = {'results': simple_merge}
	self.save_gather(output, 'iris/iris', query, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
