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

from json import loads

meta = {
	'name': 'Cluster',
	'author': 'Kaushik',
	'version': '0.1',
	'description': 'Cluster your data using kmeans and fp-growth.',
	'required': ('sklearn', 'kneed', 'mlxtend', 'numpy', 'pandas'),
	'options': (
		('json', None, False, 'Json file that contains the data', '-j', 'store', str),
		('data', None, False, 'Json object that contains the data', '-d', 'store', str),
	),
	'examples': ('cluster -j test.json')
}
	
def module_api(self):
	input_data = self.options['data']
	json_filepath = self.options['json']

	if not input_data and not json_filepath:
		return 
	elif (input_data and json_filepath) or input_data:
		data = loads(input_data)
	else:
		file_data = self._is_readable(json_filepath)
		data = loads(file_data.read())
	
	clusterer = self.cluster(data)
	output = {'json': clusterer.perform_clustering()}
	# self.save_gather(output, 'iris/cluster', json, output=self.options['output'])
	return output

def module_run(self):
	output = module_api(self)['json']
	for index, title in enumerate(output):
		print('\n')
		print(f"CLUSTER {index+1}")
		print(f"TITLE: {title}")
		print('  '+'\n  '.join(output[title]))
