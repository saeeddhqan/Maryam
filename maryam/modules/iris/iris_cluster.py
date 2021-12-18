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
    'name': 'Iris_Cluster',
    'author': 'Shaad',
    'version': '0.1',
    'description': 'Get Iris Search result and clustered results for your query',
        'required': ('Same as Iris and Cluster module'),
        'options': (
            ('query', None, True, 'Query string', '-q', 'store', str),
        ),
    'examples': ('iris_cluster -q <QUERY>')
}


def module_api(self):
    query = self.options['query']
    output_option_value = self.options['output']
    output = {}

    # Computing iris search result
    self._mode = 'api_mode'
    iris_search_result = self.opt_proc('iris', args=f'-q "{query}" --api', output='web_api')
    output['iris_search_result'] = iris_search_result

    # Computing cluster results
    clusterer = self.cluster(iris_search_result)
    output['cluster_result'] = {'json': clusterer.perform_clustering()}

    # Resetting options for iris_cluster_module
    self.options = {}
    self.options['query'] = query
    self.options['output'] = output_option_value

    self.save_gather(output, 'iris/iris_cluster', query, output=self.options['output'])
    
    return output


def module_run(self):
    output = module_api(self)
    iris_search_result = output['iris_search_result']
    cluster_result = output['cluster_result']['json']

    print('IRIS SEARCH RESULT: ')
    self.search_engine_results(iris_search_result)

    print('\n\nCLUSTER RESULT: ')
    for index, title in enumerate(cluster_result):
        print('\n')
        print(f"CLUSTER {index+1}")
        print(f"TITLE: {title}")
        print('  '+'\n  '.join(cluster_result[title]))
