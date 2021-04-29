#!/usr/bin/env python3
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


from setuptools import setup
from setuptools import find_packages

def parse_requirements():
	reqs = []
	for name in open('requirements').read().rsplit('\n'):
		if name:
			try:
				__import__(name)
			except:
				reqs.append(name)
	return reqs

setup(
	name='OWASP Maryam',
	version='2.1.5',
	url='https://github.com/saeeddhqan/Maryam',
	author='Saeed Dehqan',
	author_email='saeed.dehghan@owasp.org',
	packages=find_packages(),
	# package_data={'': package_files()},
	license='GPL-V3',
	description='OWASP Maryam is a modular/optional open source framework based on OSINT and data gathering.',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	keywords=['OWASP', 'OSINT', 'search-engine', 'social-networks', 'Maryam'],
	install_reqs=parse_requirements(),
	py_modules=['module1s','core' ,'data'],
	scripts=['maryam','scripts/script2']
)
