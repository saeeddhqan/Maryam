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

from xml.etree import ElementTree

#Using default empty strings for title and author to avoid author=None and title=None
meta = {
	'name': 'Worldcat Search',
	'author': 'Vikas Kundu',
	'version': '0.1',
	'description': 'Search books on Worldcat using author name or book title. ',
	'sources': ('Worldcat API',),
	'options': (
		('title', '', False, 'Query string for title of a book', '-t', 'store', str),
		('author', '', False, 'Query string for author of a book', '-a', 'store', str),
		('limit', 25, False, 'Search limit(number of results, default=25)', '-l', 'store', int),
		('order', 'desc', False, 'Search order(asc or desc, default=desc)', '-o', 'store', str)
	),
    'examples': ('worldcat -t <TITLE> -l 15',)
}

def module_api(self):
	# Add more error codes when found
	error_codes = {
		'102': 'No data found for this query'
	}
	title = self.options['title']
	author = self.options['author']
	limit = self.options['limit']
	order = self.options['order']
	output = {'results': []}

	run = self.worldcat(title, author, limit, order)
	if run.run_crawl() == False:
		return output
	
	xml_root = ElementTree.fromstring(run.xml_data)	

	#Parsing response code
	response_code = xml_root.findall('.//{http://classify.oclc.org}response')[0].attrib['code']
	if response_code != '4': #If not success
		if response_code in error_codes:
			self.error(f"{error_codes[response_code]}", 'worldcat', 'module_api')
		else:
			self.error('Something went wrong!', 'worldcat', 'module_api')
		return output

	#Parsing total entries available for this query
	workCount = xml_root.findall('.//{http://classify.oclc.org}workCount')
	total_entries = workCount[0].text	
	if limit > int(total_entries): 
		self.alert(f'Only {total_entries} entries available for this query instead of {limit}')
		limit = int(total_entries)

	#Parsing book data
	works = xml_root.findall('.//{http://classify.oclc.org}works')	
	output['results'] = [{} for _ in range(limit)]
	for index in range(0, limit):
    		for i in works:
        		for key,value in i[index].attrib.items():
		            output['results'][index].update({key: value})
	
	self.save_gather(output, 'search/worldcat', title, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)
	for data in output['results']:
		table_list = [[key, data[key]] for key in data.keys() ]
		self.table(table_list, ['Key', 'Value'], title=f"Entry No. {output['results'].index(data)+1}")
