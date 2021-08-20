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

from setuptools import setup, find_packages

reqs_list = [x for x in open('requirements').read().split('\n') if x and not x.startswith('#')]

setup(
	name='maryam',
	version='2.5.0',
	url='https://github.com/saeeddhqan/Maryam',
	author='Saeed Dehqan',
	author_email='saeed.dehghan@owasp.org',
	packages=find_packages(),
	include_package_data=True,
	package_data={"maryam": ['data/*']},
	license='GPL-V3',
	description='OWASP Maryam is a modular/optional open-source framework based on OSINT and data gathering.',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	keywords=['OWASP', 'OSINT', 'search-engine', 'social-networks', 'Maryam'],
	scripts=['bin/maryam'],
	install_requires=reqs_list,
	classifiers=[
		'Programming Language :: Python :: 3.8',
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Operating System :: POSIX :: Linux',
		'Environment :: Console',
	]
)

