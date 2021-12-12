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

from json import dumps
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
    output = {}
    # Executing Iris Module
    module_name = 'iris'
    iris_search_result = self.run_module_api(module_name)
    if('error' in iris_search_result.keys()):
        raise Exception(iris_search_result['error'])
    output['iris_search_result'] = iris_search_result

    # Executing Cluster module
    module_name = 'cluster'
    cluster_user_options = {
        'data': dumps(iris_search_result.get('output', None)),
        'json': None
    }
    self.set_framework_options(module_name, cluster_user_options)
    cluster_result = self.run_module_api(module_name, command_label='cluster -d <IRIS_SEARCH_RESULT>')
    if('error' in cluster_result.keys()):
        raise Exception(cluster_result['error'])
    output['cluster_result'] = cluster_result

    # Reset options in accordance with iris_cluster module
    self.options = {}
    self.options['query'] = query

    return output


def module_run(self):
    output = module_api(self)
    iris_search_result = output['iris_search_result']['output']
    cluster_result = output['cluster_result']['output']['json']

    print('IRIS SEARCH RESULT: ')
    self.search_engine_results(iris_search_result)

    print('\n\nCLUSTER RESULT: ')
    for index, title in enumerate(cluster_result):
        print('\n')
        print(f"CLUSTER {index+1}")
        print(f"TITLE: {title}")
        print('  '+'\n  '.join(cluster_result[title]))
