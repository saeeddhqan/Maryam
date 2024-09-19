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
# Hatma Suryotrisongko

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

class main:

	def __init__(self, inputfile, filetype, keyword, showcharts, verbose):

		from dask import dataframe as dd
		import json
		self.stops = open(os.path.join(BASEDIR, '../../', 'data', 'stopwords.csv')).read().split(',')

		if verbose == True:
			print("\n\n DATASET = reading file : " + inputfile)
			print("\n\n Search keyword = " + keyword)

		if filetype == "csv":
			# tmp = pd.read_csv(inputfile, header=None, low_memory=False)
			tmp = dd.read_csv(inputfile, sep=';', header=None)
			tmp2 = tmp.to_dask_array(lengths=True)
			tmp3 = tmp2.compute()
			tmp4 = pd.DataFrame(tmp3)

			if verbose == True:
				print("\n\n csv file (before preprocessing) = ")
				print(tmp4)

			self.corpus = tmp4[0].str.lower().apply(self.remove_stopwords).to_numpy()

		elif filetype == "json":
			with open(inputfile) as json_file:
				jsonfile = json.load(json_file)

			tmp = pd.DataFrame(jsonfile['results'])

			if verbose == True:
				print("\n\n json file (before preprocessing) = ")
				print(tmp)

			tmp['td'] = tmp['t'] + ' ' + tmp['d']
			self.corpus = tmp['td'].str.lower().apply(self.remove_stopwords).to_numpy()

		else:
			print('ERROR, only accept csv or json file!')

		if verbose == True:
			print('\n\n number of corpus = ')
			print(len(self.corpus))
			print('\n\n self.corpus[0] = ')
			print(self.corpus[0])
			print('\n\n all self.corpus = ')
			print(self.corpus)

		if showcharts == True:
			print('\n\n histogram of the number of words in each corpus')
			pd.Series([len(e.split()) for e in self.corpus]).hist()
			plt.show()


	def remove_stopwords(self, text):
		return ''.join([x for x in text if x not in self.stops])


	def run_sklearn_cluster_kmeans(self, selected_pretrained_model, showcharts, verbose):

		from sklearn.cluster import KMeans
		import scipy
		import umap

		pretrained_model = selected_pretrained_model
		if verbose == True:
			print('\n\n Model selection')
			# https://www.sbert.net/docs/pretrained_models.html
			print(pretrained_model)

		model = SentenceTransformer(pretrained_model)
		if verbose == True:
			print(model)

		corpus_embeddings = model.encode(self.corpus)
		if verbose == True:
			print('\n\n CORPUS EMBEDDING')
			print(corpus_embeddings.shape)
			print(corpus_embeddings)

		K = 5
		kmeans = KMeans(n_clusters=5, random_state=0).fit(corpus_embeddings)
		if verbose == True:
			print('\n\n Show Cluster using SkLearn KMeans')
			print(kmeans)

		corpus_labeled = pd.DataFrame({'ClusterLabel': kmeans.labels_, 'Sentence': self.corpus})
		print('\n\n corpus_labeled = ')
		print(corpus_labeled)

		cls_dist = pd.Series(kmeans.labels_).value_counts()
		if verbose == True:
			print('\n\n frequency of cluster label = ')
			print(cls_dist)

		distances = scipy.spatial.distance.cdist(kmeans.cluster_centers_, corpus_embeddings)
		if verbose == True:
			print("\n\n calculate distance of cluster's center point = ")
			print(distances)

		print("\n\n Cluster's center example = ")

		centers = {}
		print('Cluster', 'Size', 'Center-idx', 'Center-Example', sep='\t\t')
		for i, d in enumerate(distances):
			ind = np.argsort(d, axis=0)[0]
			centers[i] = ind
			print(i, cls_dist[i], ind, self.corpus[ind], sep="\t\t")

		if showcharts == True:
			print('\n\n Visualization of the cluster points')

			X = umap.UMAP(n_components=2, min_dist=0.0).fit_transform(corpus_embeddings)
			labels = kmeans.labels_

			fig, ax = plt.subplots(figsize=(12, 8))
			plt.scatter(X[:, 0], X[:, 1], c=labels, s=1, cmap='Paired')
			for c in centers:
				plt.text(X[centers[c], 0], X[centers[c], 1], 'CLS-' + str(c), fontsize=24)
			plt.colorbar()
			plt.show()

	def run_topic_modeling_bertopic(self, selected_pretrained_model, verbose):

		from bertopic import BERTopic

		pretrained_model = selected_pretrained_model
		if verbose == True:
			print('\n\n Model selection')
			# https://www.sbert.net/docs/pretrained_models.html
			print(pretrained_model)

		model = SentenceTransformer(pretrained_model)
		if verbose == True:
			print(model)

		corpus_embeddings = model.encode(self.corpus)
		if verbose == True:
			print('\n\n CORPUS EMBEDDING')
			print(corpus_embeddings.shape)
			print(corpus_embeddings)

		print('\n\n Topic Modeling with BERTopic')

		sentence_model = SentenceTransformer(pretrained_model)
		if verbose == True:
			print(sentence_model)

		topic_model = BERTopic(embedding_model=sentence_model)
		if verbose == True:
			print(topic_model)

		topics, _ = topic_model.fit_transform(self.corpus)
		print(topic_model.get_topic_info()[:6])
		output = topic_model.get_topic_info()

		corpus_labeled = pd.DataFrame({'ClusterLabel': topics, 'Sentence': self.corpus})
		if verbose == True:
			print("\n\n corpus_labeled = ")
			print(corpus_labeled)

		print('\n\n topics for each cluster = ')

		i = 0
		while i < len(topic_model.get_topic_info()):
			print(f"Cluster #{i} = ")
			print(topic_model.get_topic(i))
			i += 1

		return output


	def run_search_topics_top2vec(self, keyword, showcharts, verbose):

		from top2vec import Top2Vec

		print('\n\n Search Topics Using Top2Vec (caution: might not work well for a small dataset)')
		print('\n the Search Keyword = ' + keyword)

		pretrained_embedding_model = 'universal-sentence-encoder-multilingual'
		if verbose == True:
			print('\n\n Pretrained Embedding Model')
			# https://tfhub.dev/google/universal-sentence-encoder-multilingual/
			# 16 languages (Arabic, Chinese-simplified, Chinese-traditional, English, French, German, Italian, Japanese, Korean, Dutch, Polish, Portuguese, Spanish, Thai, Turkish, Russian) text encoder.
			print(pretrained_embedding_model)

		model = Top2Vec(documents=self.corpus.tolist(), speed='learn', workers=8)
		if verbose == True:
			print('\n Model = ')
			print(model)

		if model.get_num_topics() < 5:
			ntopics = model.get_num_topics()
		else:
			ntopics = 5

		topic_words, word_scores, topic_nums = model.get_topics(ntopics)
		print(topic_words)
		print(word_scores)
		print(topic_nums)

		print('\n Semantic Search Documents by Keywords = ')
		documents, document_scores, document_ids = model.search_documents_by_keywords(keywords=[keyword], num_docs=5)
		for doc, score, doc_id in zip(documents, document_scores, document_ids):
			print(f"Document: {doc_id}, Score: {score}")
			print('-----------')
			print(doc)
			print('-----------')
			print()

		if showcharts == True:
			print('\n\n Generate Word Clouds = ')
			topic_words, word_scores, topic_scores, topic_nums = model.search_topics(keywords=[keyword], num_topics=ntopics)
			for topic in topic_nums:
				model.generate_topic_wordcloud(topic)

		print('\n Similar Keywords = ')
		words, word_scores = model.similar_words(keywords=[keyword], keywords_neg=[], num_words=20)
		for word, score in zip(words, word_scores):
			print(f"{word} {score}")
