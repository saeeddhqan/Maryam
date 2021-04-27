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

from math import trunc

class main:
	def __init__(self):
		self.framework = main.framework

	def make_cite(self, url: 'URL string') -> 'cite':
		urlib = self.framework.urlib(url)
		path = urlib.path
		host = f"{urlib.scheme}://{urlib.netloc}"
		host_len = len(host)
		if path in ('', '/'):
			return host
		else:
			if host_len > 50:
				return f"{host} › ..."
		if '?' in path:
			path = path[:path.rfind('?')]
		if '.' in path:
			path = path[:path.rfind('.')]
		suffix = ''
		if path[:22] != urlib.path:
			suffix = '...'
		path = path[:-1] if path.endswith('/') else path
		path = path.replace('/', ' › ')[:22] + suffix
		cite = f"{host}{path}"
		return cite

	def compute_count_consensus( 
			e: dict(type=list, help='list of search engines sorted by quality'),
			l: dict(type=int, help='number of results')) -> 'a list of numbers':
		x=len(e)
		o={}
		for i in e:
			o[i]=trunc(l/x)
		l-=l-(l%x)
		if l!=0:
			if l<x:
				for i in range(l):
					o[e[i]]+=1
		return o
