# TESTED USING =
# topicmodeling -i mixed.json -t json -m all-distilroberta-v1
# topicmodeling -i mixed.json -t json -s -v -m all-distilroberta-v1
# topicmodeling -i mixed.json -t json -s -m all-distilroberta-v1
# topicmodeling -i mixed.json -t json -v -m all-distilroberta-v1
# topicmodeling -i testdataset.csv -t csv -m all-mpnet-base-v2
# topicmodeling -i testdataset.csv -t csv -s -v -m all-mpnet-base-v2
# topicmodeling -i testdataset.csv -t csv -s -m all-mpnet-base-v2
# topicmodeling -i testdataset.csv -t csv -v -m all-mpnet-base-v2
# Note: download the dataset for testing from https://github.com/keamanansiber/Maryam/tree/master/notebooks


meta = {
	'name': 'Topic Modeling',
	'author': 'Hatma Suryotrisongko',
	'version': '0.1.0',
	'description': 'Topic Modeling Algorithms.',
	'options': (
		('inputfile', None, True, 'Input file that contains the data', '-i', 'store', str),
		('filetype', None, True, 'File type: csv/json', '-t', 'store', str),
		('showcharts', None, False, 'Show charts?', '-s', 'store_true', bool),
		('verbose', None, False, 'Verbose output?', '-v', 'store_true', bool),
		('pretrained_model', None, True, 'model for embedding', '-m', 'store', str),
	),
	'examples': ('topicmodeling -i mixed.json -t json -s True -v False -m all-mpnet-base-v2')
}


def module_api(self):

	run = self.topic(self.options['inputfile'], self.options['filetype'], self.options['showcharts'], self.options['verbose'])
	run.run_sklearn_cluster_kmeans(self.options['pretrained_model'], self.options['showcharts'], self.options['verbose'])
	run.run_topic_modeling_bertopic(self.options['pretrained_model'], self.options['verbose'])


def module_run(self):
	module_api(self)