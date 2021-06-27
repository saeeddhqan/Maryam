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
	'name': 'Article Search',
	'author': 'Kaushik',
	'version': '0.1',
	'description': 'Search for scientific papers and articles from Google Scholar \
			, Arxiv, Pubmed, and Core.ac.uk',
	'sources': ('scholar', 'arxiv', 'pubmed', 'core_ac'),
	'options': (
		('query', None, True, 'Search query for papers or articles', '-q', 'store', str),
		('limit', 15, False, 'Max result count (default=15)', '-l', 'store', int),
		('exclude medical', False, False, 'Exclude medical results', '-e', 'store_true', bool),
	),
	'examples': ('article_search -q <query>', 'article_search -q <query> --output')
}

def module_api(self):
	q = self.options['query']
	no_medical = self.options['exclude medical']
	limit = self.options['limit']//3 if no_medical else self.options['limit']//4

	scholar = self.scholar(q, limit)
	scholar.run_crawl()
	results = scholar.results

	core_ac = self.core_ac(q, limit)
	core_ac.run_crawl()
	results.extend(core_ac.results)

	arxiv = self.arxiv(q, limit)
	arxiv.run_crawl()
	results.extend(arxiv.results)

	if not no_medical:
		pubmed = self.pubmed(q, limit)
		pubmed.run_crawl()
		results.extend(pubmed.results)

	output = {'results': results}

	self.save_gather(output, 'osint/article_search', q, output=self.options['output'])
	return output

def module_run(self):
	self.search_engine_results(module_api(self))
