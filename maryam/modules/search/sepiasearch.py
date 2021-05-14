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
	'name': 'sepiasearch',
	'author': 'Rishabh Jain',
	'version': '0.1',
	'description': "Sepia Search is a video search engine optimized for PeerTube channels.",
	'sources': ('sepiasearch',),
	'options': (
		('query', None, True, 'Query string', '-q', 'store', str),
		('limit', 15, False, 'Max result count (default=15)', '-l', 'store', int),
	),
	'examples': ('sepiasearch -q <QUERY> -l 15 --output',)
}

def module_api(self):
    query = self.options['query']
    limit = self.options['limit']
    run = self.sepiasearch(query, limit)
    run.run_crawl()
    output = {}
    count = run.total_result_found
    data = run.collected_data
    if count:
        output['Total Results'] = count 

    output['results'] = []
    
    if data:
        output['results'].extend(data)
    
    self.save_gather(output, 'search/sepiasearch', query, output=self.options['output'])
    return output
    
def module_run(self):
    self.alert_results(module_api(self))