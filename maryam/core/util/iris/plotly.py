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

import plotly

class main:

	def __init__(self):
		""" a class for plotly framework. currently it just supports common methods """
		self.framework = main.framework

	def tf_pie(self, docs: 'documents', form: 'documet form. e.g html',
				last: 'number of words', without_punc=True, remove_stopwords=False):
		tf = self.framework.tf_histogram(docs, form, without_punc)
		if remove_stopwords:
			tf.remove_stopwords()
		bow = tf._counter(last)
		values = []
		labels = []
		for word, count in bow:
			values.append(count)
			labels.append(word)
		fig = plotly.graph_objects.Figure(plotly.graph_objects.Pie(values=values,labels=labels,
			texttemplate = "%{label}: %{value:s} <br>(%{percent})",
			textposition = "inside"))
		fig.show()
