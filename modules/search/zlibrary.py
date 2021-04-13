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

from bs4 import BeautifulSoup

# Using default empty strings for query, lang, ext to avoid &ext=None etc.
meta = {
	'name': 'Zlibrary Search',
	'author': 'Vikas Kundu',
	'version': '0.1',
	'description': 'Search books and articles on Zlibrary . ',
	'sources': ('Zlibrary',),
	'options': (
		('query', '', True, 'Query string to search for', '-q', 'store', str),
		('exact', False, False, 'Search for exact query(True or False, default=False)', '-e', 'store_true', bool),
		('start_year', 0, False, 'Year to start search from(min: 1800 onwards)', '-sy', 'store', int),
		('end_year', 0, False, 'Year till which to search for(max: present year)', '-ey', 'store', int),
		('lang', '', False, 'Language in which to search(i.e. English)', '-ln', 'store', str),
		('ext', '', False, 'Extension of the ebook or article(i.e. pdf, epub, txt, rar, mobi)', '-ex', 'store', str),
		('count', 50, False, 'No. of results to show(default=50)', '-c', 'store', int) # 50 entries per page
	),
    'examples': ('zlibrary -q <QUERY> -ex pdf',)
}

def table_format(data):
 	# Declaring output_table here in case no table found on page, return this one
	output_table = []
	raw_data = BeautifulSoup(data, 'html.parser')
	for table in raw_data.find_all('table', {'class': 'table_book'}):	
		# If this statement is not used, table will reset each time and only 50 entries will be there
		if output_table == []:
			output_table = [ {header.text:[]} for header in table.findAll('th', {'class': 'header'}) ]
		for row in table.find_all('tr'):
			# Using zip to avoid cartesian product caused by 2 loops
			for row_data, column in zip(row.find_all('td'), output_table):
				 # Using split to clean the data and remove trailing spaces, /n, etc.
				row_data = ' '.join(row_data.text.split())
				 # Find the key of present column
				key = [ i for i in column.keys() ][0]
				# Adding entire row data in one dump to a column
				column[key].append(row_data) 
	return output_table

def module_api(self):
	query = self.options['query']
	exact = self.options['exact']
	start_year = self.options['start_year']
	end_year = self.options['end_year']
	lang = self.options['lang']
	extension = self.options['ext']
	count = self.options['count'] 
	output = {'results': [ {'books':[]}, {'articles':[]} ] }

	run = self.zlibrary(query, exact, start_year, end_year, lang, extension, count)
	if run.search() == 'False':
		return output
	
	books_table = table_format(run.books_data)
	articles_table = table_format(run.articles_data)

	
	output['results'][0]['books']	= books_table
	output['results'][1]['articles'] = articles_table
	
	self.save_gather(output, 'search/zlibrary', query, output=self.options.get('output'))
	return output

def module_run(self):
	output = module_api(self)

	for src in ['books', 'articles']:
		pos = ['books', 'articles'].index(src) # Index to see books data or articles data
		base = output['results'][pos][src] # The base to access items
		columns = rows = []

		no_of_columns = len(base)
		no_of_rows =  0 if len(base) == 0 else \
		len([ i for i in base[0].values() ][0])
		# Populating table headers
		columns = [j for i in base for j in i.keys() ] 
		
		# Using double loop to format data for table
		for row_index in range(0, no_of_rows): 
			temp = []
			for col_index in range(0, no_of_columns):
				key_name = columns[col_index]
				temp.append(base[col_index][key_name][row_index]) 
			rows.append(temp) # Dump one row in the rows
		
		# Otherwise core will throw error if self.table is given 0 input
		if no_of_columns == 0:
			self.table([], ['No output'], title=f"{src}")
		else:
			self.table(rows, columns, title=f'{src}')
		
