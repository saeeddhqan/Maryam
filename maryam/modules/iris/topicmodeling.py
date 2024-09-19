# modules/iris/topicmodeling.py
# # TESTING The Main Function =
# topicmodeling -i mixed.json -t json -m all-distilroberta-v1
# topicmodeling -i mixed.json -t json -s -v -m all-distilroberta-v1
# topicmodeling -i mixed.json -t json -s -m all-distilroberta-v1
# topicmodeling -i mixed.json -t json -v -m all-distilroberta-v1
# topicmodeling -i testdataset.csv -t csv -m all-mpnet-base-v2
# topicmodeling -i testdataset.csv -t csv -s -v -m all-mpnet-base-v2
# topicmodeling -i testdataset.csv -t csv -s -m all-mpnet-base-v2
# topicmodeling -i testdataset.csv -t csv -v -m all-mpnet-base-v2
# # TESTING The Reporting & API Function =
# topicmodeling -i mixed.json -t json -m all-distilroberta-v1 --output
# report json testreport iris/topicmodeling
# topicmodeling -i mixed.json -t json -m all-distilroberta-v1 --api
# # TESTING The Function: Search Topics Using a Keyword (Top2Vec) =
# topicmodeling -i mixed.json -t json -m all-distilroberta-v1 -k music
# Note: download the dataset for testing from https://github.com/keamanansiber/Maryam/tree/master/notebooks
# Hatma Suryotrisongko


meta = {
	'name': 'Topic Modeling',
	'author': 'Hatma Suryotrisongko',
	'version': '0.1.0',
	'description': 'Topic Modeling Algorithms.',
	'required': ('dask', 'scikit-learn', 'umap', 'bertopic', 'gensim', 'top2vec'),
	'options': (
		('inputfile', None, True, 'Input file that contains the data', '-i', 'store', str),
		('filetype', None, True, 'File type: csv/json', '-t', 'store', str),
		('keyword', None, False, 'Search keyword: ', '-k', 'store', str),
		('showcharts', None, False, 'Show charts?', '-s', 'store_true', bool),
		('verbose', None, False, 'Verbose output?', '-v', 'store_true', bool),
		('pretrained_model', None, True, 'model for embedding', '-m', 'store', str),
	),
	'examples': ('topicmodeling -i mixed.json -t json -k music -s True -v False -m all-mpnet-base-v2')
}


def module_api(self):

	run = self.topic(self.options['inputfile'], self.options['filetype'], self.options['keyword'], self.options['showcharts'], self.options['verbose'])
	run.run_sklearn_cluster_kmeans(self.options['pretrained_model'], self.options['showcharts'], self.options['verbose'])

	results = run.run_topic_modeling_bertopic(self.options['pretrained_model'], self.options['verbose'])
	self.output("\n\nResults = \n")
	self.output( results )

	output = {'results': results.to_json(orient="records") }

	inputfile = self.options['inputfile']
	self.save_gather(output, 'iris/topicmodeling', inputfile, output=self.options['output'])

	if self.options['keyword'] is not None:
		self.output(" keyword = " + self.options['keyword'])
		run.run_search_topics_top2vec(self.options['keyword'], self.options['showcharts'], self.options['verbose'])

	return output


def module_run(self):
	output = module_api(self)
	self.output("\n\nOutput = \n")
	self.output( output )
