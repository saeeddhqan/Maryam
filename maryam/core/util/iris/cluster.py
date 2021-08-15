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
import json
from time import time
from html import unescape

from maryam.core.basedir import BASEDIR

class main:

	def __init__(self, input_json):
		""" Perform clustering on a set of documents """
		self.framework = main.framework
		self.json = input_json

	def remove_stopwords(self, text):
		stops = open(os.path.join(BASEDIR, 'data', 'stopwords.csv')).read().split(',')
		return [x for x in text if x not in stops]

	def tokenize_and_stem(self, text):
		tokens = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",text)
		filtered_tokens = []
		for token in tokens:
			if re.search('[a-zA-Z]', token):
				filtered_tokens.append(token.lower())
		return ' '.join(filtered_tokens)

	def punc(self, docs):
		toreturn = []
		for word in self.remove_stopwords(re.findall(r"[\w\-_#]+", docs)):
			if not word.isnumeric():
				toreturn.append(word)
		return ' '.join(toreturn)
	
	def get_frequent_itemsets(self, dataset):
		import pandas as pd
		from mlxtend.frequent_patterns import fpgrowth
		from mlxtend.preprocessing import TransactionEncoder

		te = TransactionEncoder()
		te_ary = te.fit_transform(dataset)
		dataset = pd.DataFrame(te_ary, columns=te.columns_)
		freq_itemsets = fpgrowth(dataset, min_support=0.2, use_colnames=True)
		freq_itemsets = freq_itemsets.sort_values('support', ascending=False)['itemsets']
		freq_itemsets = list(filter(lambda x:len(x)>1, freq_itemsets.values.tolist()))
		return freq_itemsets

	def perform_preprocess(self):
		self.df['d'] = self.df['t'] + ' ' + self.df['d']
		self.df['d'] = self.df['d'].apply(self.tokenize_and_stem).apply(self.punc)

	def perform_clustering(self):
		import pandas as pd

		from sklearn.cluster import KMeans
		from sklearn.feature_extraction.text import TfidfVectorizer

		from kneed import KneeLocator

		self.framework.verbose('Loading Data')
		self.df = pd.DataFrame(self.json['results'])

		self.framework.verbose('Preprocessing')
		self.perform_preprocess()

		vectorizer = TfidfVectorizer(max_features=20, min_df=0.2)
		X = vectorizer.fit_transform(self.df['d'])

		self.framework.verbose('Clustering with KMeans')
		inertias = []
		fitted = []

		for cluster_count in range(1,20):
			km = KMeans(n_clusters=cluster_count)
			km.fit(X)
			inertias.append(km.inertia_)
			fitted.append(km)

		kn = KneeLocator(range(1, len(inertias)+1), inertias, curve='convex', direction='decreasing')
		optimal_k = kn.knee

		best_fit_index = optimal_k-1
		km = fitted[best_fit_index]

		terms = vectorizer.get_feature_names()
		order_centroids = km.cluster_centers_.argsort()[:, ::-1]

		summaries = [[] for _ in range(optimal_k)]
		titles = [[] for _ in range(optimal_k)]
		for i in range(optimal_k):
			for index, cluster in enumerate(km.labels_.tolist()):
				if cluster == i:
					summaries[i].append(self.df['d'][index])
					titles[i].append(self.df['t'][index])

		self.framework.verbose('Assigning titles to clusters')
		results = {}
		for index, cluster in enumerate(summaries):
			d = list(map(lambda x: x.split(), cluster))
			self.framework.verbose(f'Assigning title {index+1}')
			probable_titles = self.get_frequent_itemsets(d)
			cluster_title = ' | '.join(list(map(lambda x: ' '.join(list(x)), probable_titles))[:5])
			
			results[cluster_title] = titles[index]
		return results
