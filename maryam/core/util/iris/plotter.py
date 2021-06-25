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

#### Historgram Imports
import pandas as pd
import matplotlib.pyplot as plt
import re # Used by filters too
from collections import Counter # Used by filters too
from nltk.corpus import stopwords # Used by filters too

#### Plotly imports
import plotly.graph_objects as go

#### Wordcloud imports
from wordcloud import WordCloud

#### Class filters ends
class filters:
	def __init__(self, docs, form, limit=20, without_punc=True, remove_stopwords=False):
		self._framework = main.framework
		self._form = form.lower()
		self._docs = docs.lower()
		self._limit = limit
		self._without_punc = without_punc
		self._remove_stopwords = remove_stopwords
		self._words = self._docs.split()

		if self._form == 'html':
			self._remove_html()
		if self._without_punc:
			self._remove_punc()
		if self._remove_stopwords:
			self._remove_stopwords

	def _remove_stopwords(self):
		try:
			stops = stopwords.words('english')
		except LookupError:
			import nltk
			nltk.download('stopwords')
		finally:
			stops = stopwords.words('english')
			self._words = [x for x in self._words if x not in stops]
	
	def _remove_punc(self):
		self._words = re.findall(r"[\w\-_#]+", self._docs)

	def _remove_html(self):
		pp = self._framework.page_parse(self._docs)
		pp.remove_html_tags
		self._docs = pp.page

	def _limit_words(self):
		bow = Counter(self._words)
		return bow.most_common(self._limit)

	@property
	def filtered_words(self):
		return self._words

	@property
	def most_common(self):
		return self._limit_words()

######## Class filters starts

######## Class Historgram starts

class histogram:

	def __init__(self, docs: 'documents', form: 'documet form. e.g html', limit: 'number of words', 
	without_punc=True, remove_stopwords=False):
		""" show histogram plot of web term frequency """
		f = filters(docs, form, limit, without_punc)
		self.words = f.filtered_words
		self.most_common = f.most_common


	def plot_histogram(self, title):
		clean_tweets_no_urls = pd.DataFrame(self.most_common,
						columns=['words', 'count'])
		fig, ax = plt.subplots(figsize=(25, 25))
		clean_tweets_no_urls.sort_values(by='count').plot.barh(x='words',
									y='count',
									ax=ax,
									color="black")
		ax.set_title(title)
		plt.show()


######## Class Historgram ends

######## Class Plotly starts

class plotly:

	def __init__(self, docs: 'documents', form: 'documet form. e.g html', limit: 'number of words', 
	without_punc=True, remove_stopwords=False):
		f = filters(docs, form, limit, without_punc, remove_stopwords)
		self.bow = f.most_common
		
	def plot_pie(self, title):
		values = []
		labels = []
		for word, count in self.bow:
			values.append(count)
			labels.append(word)
		fig = go.Figure(go.Pie(title=title,values=values,labels=labels,
			texttemplate = "%{label}: %{value:$,s} <br>(%{percent})",
			textposition = "inside"))
		fig.show()

######## Class Plotly ends

######## Class Wordcloud starts

class wcloud:
	def __init__(self, docs: 'documents', form: 'documet form. e.g html', limit: 'number of words', 
	without_punc=True, remove_stopwords=False):
		f = filters(docs, form, limit, without_punc, remove_stopwords)
		self.bow = f.most_common
		
	def plot_wcloud(self, title):
		cloud_data = ' '.join(i[0] for i in self.bow)
		wcd = WordCloud().generate(cloud_data)
		plt.imshow(wcd, interpolation='bilinear')
		plt.axis("off")
		plt.title(title)
		plt.show()

######## Class Wordcloud ends

class main:
	def __init__(self, plot_dict):
		self.plot_type = plot_dict['plot_type']
		self.data = plot_dict['data']
		self.data_type = plot_dict['data_type'] \
		if plot_dict['data_type'] in plot_dict else 'html'

		self.plot_title = plot_dict['plot_title'] \
		if plot_dict['plot_title'] in plot_dict else ''

		self.limit = plot_dict['limit'] \
		if plot_dict['limit'] in plot_dict else 20

		self.remove_punc =  plot_dict['remove_punc'] \
		if plot_dict['remove_punc'] in plot_dict else True		

		self.remove_stopwords =  plot_dict['remove_stopwords'] \
		if plot_dict['remove_stopwords'] in plot_dict else False
			
		if 'histogram' in self.plot_type:
			hstgrm = histogram(self.data, self.data_type, self.limit, self.remove_punc, self.remove_stopwords)
			hstgrm.plot_histogram(self.plot_title)
			
		if 'piechart' in self.plot_type:
			pie = plotly(self.data, self.data_type, self.limit, self.remove_punc, self.remove_stopwords)
			pie.plot_pie(self.plot_title)
		
		if 'wordcloud' in self.plot_type:
			w = wcloud(self.data, self.data_type, self.limit, self.remove_punc, self.remove_stopwords)
			w.plot_wcloud(self.plot_title)
	

