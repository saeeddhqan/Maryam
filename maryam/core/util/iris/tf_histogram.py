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

import pandas as pd
import matplotlib.pyplot as plt
import re

from collections import Counter
from nltk.corpus import stopwords

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
		if self.without_punc:
			self._punc()
		self.words = self.docs.split()

	def remove_stopwords(self):
		stops = stopwords.words('english')
		self.words = [x for x in self.words if x not in stops]

	def _punc(self):
		self.words = re.findall(r"[\w\-_#]+", self.docs)

	def _counter(self, last):
		""" last: number of terms to show in plot """
		bow = Counter(self.words)
		return bow.most_common(last)

	def plot_histogram(self, title, last):
		most_common = self._counter(last)
		clean_tweets_no_urls = pd.DataFrame(most_common,
						columns=['words', 'count'])
		fig, ax = plt.subplots(figsize=(25, 25))
		clean_tweets_no_urls.sort_values(by='count').plot.barh(x='words',
									y='count',
									ax=ax,
									color="black")
		ax.set_title(title)
		plt.show()
