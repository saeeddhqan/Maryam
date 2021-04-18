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

class main:
	def __init__(self):
		self.framework = main.framework

	def make_cite(self, url: 'URL string') -> 'cite':
		default_pages = ['index']
		urlib = self.framework.urlib(url)
		path = urlib.path
		host = f"{urlib.scheme}://{urlib.netloc}"
		host_len = len(host)
		if path in ('', '/'):
			return host
		else:
			if host_len > 50:
				return f"{host} › ..."
		path_join = []
		if '?' in path:
			path = path[:path.rfind('?')]
		counter = 0
		path_split = path.split('/')
		path_split = path_split[:3] + ['...'] if len(path_split) > 3 else path_split 
		for section in path_split:	
			if not section or section == ' ':
				continue
			if '.' in section and section != '...':
				section = section[:section.rfind('.')]
			if section not in default_pages and len(section) > 1:
				if len(section) > 22:
					path_join.append(f"{section[:22]}...")
					break
				counter += len(section)
				if counter > 30:
					path_join.append(f"{section[:27]}...")
					break
				path_join.append(section)
			else:
				path_join.append('...')
				break
		path = '/'.join(path_join)
		path = path.replace('/', ' › ')
		cite = f"{host} › {path}"
		return cite
