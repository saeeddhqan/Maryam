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
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class main:	
	def __init__(self):	
		self.framework = main.framework

	def _remove_url(self, data):
		return re.sub(r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", '', data)	
	
	def plot_wcloud(self, title, docs: 'documents', form: 'documet form. e.g html', limit: 'number of words', 
	without_punc=True, remove_stopwords=False, should_show=True):
		docs = str(docs)
		docs = self._remove_url(docs)
		tf = self.framework.tf_histogram(docs, form, without_punc)

		if remove_stopwords:
			tf.remove_stopwords()
		bow = tf._counter(limit)
		cloud_data = ' '.join(i[0] for i in bow)

		if not cloud_data:
			self.framework.error('NoDataToPrintError.', 'util/iris/word_cloud', 'plot_wcloud')
			return False

		wcd = WordCloud().generate(cloud_data)
		plt.imshow(wcd, interpolation='bilinear')
		plt.axis("off")
		plt.title(title)
		filename = os.path.join(self.framework.workspace,title.replace(' ','_')+'.png')
		plt.savefig(filename, format="png")
		if should_show:
			plt.show()

		return filename

