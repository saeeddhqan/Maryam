# core/util/iris/topicmodeling.py
# Based on Hatma Suryotrisongko's prototype = https://github.com/keamanansiber/Maryam/blob/master/notebooks/Prototype_4_TopicModeling_0_1_0_CsvFile_Options_StopwordsRemoval_27062022.ipynb

import pandas as pd
import numpy as np
import json
import csv
from dask import dataframe as dd

from sklearn.cluster import KMeans
import scipy
import matplotlib.pyplot as plt
import umap

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS


class main:

    def __init__(self, inputfile, filetype, showcharts, verbose):

        if verbose == True:
            print("\n\n DATASET = reading file : " + inputfile)

        if filetype == "csv":
            # tmp = pd.read_csv(inputfile, header=None, low_memory=False)
            tmp = dd.read_csv(inputfile, sep=';', header=None)
            tmp2 = tmp.to_dask_array(lengths=True)
            tmp3 = tmp2.compute()
            tmp4 = pd.DataFrame(tmp3)

            if verbose == True:
                print("\n\n csv file (before preprocessing) = ")
                print(tmp4)

            self.corpus = tmp4[0].str.lower().apply(remove_stopwords).to_numpy()

        elif filetype == "json":
            with open(inputfile) as json_file:
                jsonfile = json.load(json_file)

            tmp = pd.DataFrame(jsonfile['results'])

            if verbose == True:
                print("\n\n json file (before preprocessing) = ")
                print(tmp)

            tmp['td'] = tmp['t'] + ' ' + tmp['d']
            self.corpus = tmp['td'].str.lower().apply(remove_stopwords).to_numpy()

        else:
            print("ERROR, only accept csv or json file!")

        if verbose == True:
            print("\n\n number of corpus = ")
            print(len(self.corpus))
            print("\n\n self.corpus[0] = ")
            print(self.corpus[0])
            print("\n\n all self.corpus = ")
            print(self.corpus)

        if showcharts == True:
            print("\n\n histogram of the number of words in each corpus")
            pd.Series([len(e.split()) for e in self.corpus]).hist()
            plt.show()

    def run_sklearn_cluster_kmeans(self, selected_pretrained_model, showcharts, verbose):

        pretrained_model = selected_pretrained_model
        if verbose == True:
            print("\n\n Model selection")
            # https://www.sbert.net/docs/pretrained_models.html
            print(pretrained_model)

        model = SentenceTransformer(pretrained_model)
        if verbose == True:
            print(model)

        corpus_embeddings = model.encode(self.corpus)
        if verbose == True:
            print("\n\n CORPUS EMBEDDING")
            print(corpus_embeddings.shape)
            print(corpus_embeddings)

        K = 5
        kmeans = KMeans(n_clusters=5, random_state=0).fit(corpus_embeddings)
        if verbose == True:
            print("\n\n Show Cluster using SkLearn KMeans")
            print(kmeans)

        corpus_labeled = pd.DataFrame({'ClusterLabel': kmeans.labels_, 'Sentence': self.corpus})
        print("\n\n corpus_labeled = ")
        print(corpus_labeled)

        cls_dist = pd.Series(kmeans.labels_).value_counts()
        if verbose == True:
            print("\n\n frequency of cluster label = ")
            print(cls_dist)

        distances = scipy.spatial.distance.cdist(kmeans.cluster_centers_, corpus_embeddings)
        if verbose == True:
            print("\n\n calculate distance of cluster's center point = ")
            print(distances)

        print("\n\n Cluster's center example = ")

        centers = {}
        print("Cluster", "Size", "Center-idx", "Center-Example", sep="\t\t")
        for i, d in enumerate(distances):
            ind = np.argsort(d, axis=0)[0]
            centers[i] = ind
            print(i, cls_dist[i], ind, self.corpus[ind], sep="\t\t")

        if showcharts == True:
            print("\n\n Visualization of the cluster points")

            X = umap.UMAP(n_components=2, min_dist=0.0).fit_transform(corpus_embeddings)
            labels = kmeans.labels_

            fig, ax = plt.subplots(figsize=(12, 8))
            plt.scatter(X[:, 0], X[:, 1], c=labels, s=1, cmap='Paired')
            for c in centers:
                plt.text(X[centers[c], 0], X[centers[c], 1], "CLS-" + str(c), fontsize=24)
            plt.colorbar()
            plt.show()

    def run_topic_modeling_bertopic(self, selected_pretrained_model, verbose):

        pretrained_model = selected_pretrained_model
        if verbose == True:
            print("\n\n Model selection")
            # https://www.sbert.net/docs/pretrained_models.html
            print(pretrained_model)

        model = SentenceTransformer(pretrained_model)
        if verbose == True:
            print(model)

        corpus_embeddings = model.encode(self.corpus)
        if verbose == True:
            print("\n\n CORPUS EMBEDDING")
            print(corpus_embeddings.shape)
            print(corpus_embeddings)

        print("\n\n Topic Modeling with BERTopic")

        sentence_model = SentenceTransformer(pretrained_model)
        if verbose == True:
            print(sentence_model)

        topic_model = BERTopic(embedding_model=sentence_model)
        if verbose == True:
            print(topic_model)

        topics, _ = topic_model.fit_transform(self.corpus)
        print(topic_model.get_topic_info()[:6])

        corpus_labeled = pd.DataFrame({'ClusterLabel': topics, 'Sentence': self.corpus})
        if verbose == True:
            print("\n\n corpus_labeled = ")
            print(corpus_labeled)

        print("\n\n topics for each cluster = ")

        i = 0
        while i < len(topic_model.get_topic_info()):
            print("Cluster #" + str(i) + " = ")
            print(topic_model.get_topic(i))
            i += 1

