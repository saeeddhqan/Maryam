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

import re
import os
from collections import Counter
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

class main:

	def __init__(self, docs: 'documents', form: 'documet form. e.g html', without_punc=True):
		""" show histogram plot of web term frequency """
		self.framework = main.framework
		self.form = form.lower()
		self.docs = docs.lower()
		self.without_punc = without_punc
		if self.form == 'html':
			pp = self.framework.page_parse(self.docs)
			pp.remove_html_tags
			self.docs = pp.page
		self.words = self.docs.split()
		if self.without_punc:
			self._punc()

	def remove_stopwords(self, rest):
		stops = open(os.path.join(BASEDIR, '../../', 'data', 'stopwords.csv')).read().split(',')
		self.words = [x for x in self.words if x not in stops and x not in rest]

	def _punc(self):
		self.words = re.findall(r"[\w\-_#]{2,}", self.docs)

	def _counter(self, last):
		""" last: number of terms to show in plot """
		bow = Counter(self.words)
		return bow.most_common(last)

	def plot_histogram(self, title, last, should_show=False):
		import pandas as pd
		import matplotlib.pyplot as plt

		most_common = self._counter(last)
		clean_tweets_no_urls = pd.DataFrame(most_common,
						columns=['words', 'count'])
		fig, ax = plt.subplots(figsize=(25, 25))
		clean_tweets_no_urls.sort_values(by='count').plot.barh(x='words',
									y='count',
									ax=ax,
									color="black")
		ax.set_title(title)

		filename = os.path.join(self.framework.workspace,title.replace(' ','_')+'.png')
		plt.savefig(filename, format="png")

		if should_show:
			plt.show()

		return filename
