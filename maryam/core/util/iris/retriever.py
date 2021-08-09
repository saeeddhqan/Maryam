#!/usr/bin/env python3
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

class main:
	"""
	A scikit-learn estimator for TfidfRetriever. Trains a tf-idf matrix from a corpus
	of documents then finds the most N similar documents of a given input document by
	taking the dot product of the vectorized input document and the trained tf-idf matrix.

	Parameters
	----------
	lowercase : boolean
		Convert all characters to lowercase before tokenizing. (default is True)
	preprocessor : callable or None
		Override the preprocessing (string transformation) stage while preserving
		the tokenizing and n-grams generation steps. (default is None)
	tokenizer : callable or None
		Override the string tokenization step while preserving the preprocessing
		and n-grams generation steps (default is None)
	stop_words : string {‘english’}, list, or None
		If a string, it is passed to _check_stop_list and the appropriate stop
		list is returned. ‘english’ is currently the only supported string value.
		If a list, that list is assumed to contain stop words, all of which will
		be removed from the resulting tokens.
		If None, no stop words will be used. max_df can be set to a value in the
		range [0.7, 1.0) to automatically detect and filter stop words based on
		intra corpus document frequency of terms.
		(default is None)
	token_pattern : string
		Regular expression denoting what constitutes a “token”. The default regexp
		selects tokens of 2 or more alphanumeric characters (punctuation is completely
		ignored and always treated as a token separator).
	ngram_range : tuple (min_n, max_n)
		The lower and upper boundary of the range of n-values for different n-grams
		to be extracted. All values of n such that min_n <= n <= max_n will be used.
		(default is (1, 1))
	max_df : float in range [0.0, 1.0] or int
		When building the vocabulary ignore terms that have a document frequency strictly
		higher than the given threshold (corpus-specific stop words). If float, the parameter
		represents a proportion of documents, integer absolute counts. This parameter is
		ignored if vocabulary is not None. (default is 1.0)
	min_df : float in range [0.0, 1.0] or int
		When building the vocabulary ignore terms that have a document frequency
		strictly lower than the given threshold. This value is also called cut-off
		in the literature. If float, the parameter represents a proportion of
		documents, integer absolute counts. This parameter is ignored if vocabulary
		is not None. (default is 1)
	vocabulary : Mapping or iterable, optional
		Either a Mapping (e.g., a dict) where keys are terms and values are indices
		in the feature matrix, or an iterable over terms. If not given, a vocabulary
		is determined from the input documents. (default is None)
	paragraphs : iterable
		an iterable which yields either str, unicode or file objects
	top_n : int (default 20)
		maximum number of top articles (or paragraphs) to retrieve
	verbose : bool, optional
		If true, all of the warnings related to data processing will be printed.

	Attributes
	----------
	vectorizer : TfidfVectorizer
		See https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
	tfidf_matrix : sparse matrix, [n_samples, n_features]
		Tf-idf-weighted document-term matrix.

	Examples
	--------
	>>> retriever = TfidfRetriever(ngram_range=(1, 2), max_df=0.85, stop_words='english')
	>>> retriever.fit(X=df)
	>>> best_idx_scores = retriever.predict(X='A question or text for which retriever will find closest match')
	"""

	def __init__(
		self,
		lowercase=True,
		preprocessor=None,
		tokenizer=None,
		stop_words="english",
		token_pattern=r"(?u)\b\w\w+\b",
		ngram_range=(1, 2),
		max_df=1,
		min_df=0,
		vocabulary=None,
		top_n=20,
		verbose=False,
	):
		from sklearn.feature_extraction.text import TfidfVectorizer

		self.framework = main.framework
		self.lowercase = lowercase
		self.preprocessor = preprocessor
		self.tokenizer = tokenizer
		self.stop_words = stop_words
		self.token_pattern = token_pattern
		self.ngram_range = ngram_range
		self.max_df = max_df
		self.min_df = min_df
		self.vocabulary = vocabulary
		self.top_n = top_n
		self.verbose = verbose

		vectorizer = TfidfVectorizer(
			lowercase=self.lowercase,
			preprocessor=self.preprocessor,
			tokenizer=self.tokenizer,
			stop_words=self.stop_words,
			token_pattern=self.token_pattern,
			ngram_range=self.ngram_range,
			max_df=self.max_df,
			min_df=self.min_df,
			vocabulary=self.vocabulary,
		)
		self.vectorizer = vectorizer

	def fit(self, df, y=None):
		self.metadata = df
		self.tfidf_matrix = self.vectorizer.fit_transform(list(map(' '.join, df["pages"])))
		return self

	def predict(self, query: str) -> 'OrderedDict':
		"""
		Compute the top_n closest documents given a query

		Parameters
		----------
		query: str

		Returns
		-------
		best_idx_scores: OrderedDict
			Dictionnaire with top_n best scores and idices of the documents as keys

		"""
		import time
		import prettytable
		from collections import OrderedDict

		t0 = time.time()
		scores = self._compute_scores(query)
		idx_scores = [(idx, score) for idx, score in enumerate(scores)]
		best_idx_scores = OrderedDict(
			sorted(idx_scores, key=(lambda tup: tup[1]), reverse=True)[: self.top_n]
		)
		closest_docs_indices = list(best_idx_scores.keys())

		if self.verbose:
			rank = 1
			table = prettytable.PrettyTable(["rank", "index", "title"])
			for i in range(len(closest_docs_indices)):
				index = closest_docs_indices[i]
				# if self.paragraphs:
				#	  article_index = self.paragraphs[int(index)]["index"]
				#	  title = self.metadata.iloc[int(article_index)]["title"]
				# else:
				title = self.metadata.iloc[int(index)]["title"]
				table.add_row([rank, index, title])
				rank += 1
			print(table)
			print("Time: {} seconds".format(round(time.time() - t0, 5)))

		return best_idx_scores

	def _compute_scores(self, query):
		question_vector = self.vectorizer.transform([query])
		scores = self.tfidf_matrix.dot(question_vector.T).toarray()
		return scores

	def filter_pages(
		self,
		articles,
		drop_empty=True,
		read_threshold=1000,
		public_data=True,
		min_length=0,
		max_length=5000,
	):
		"""
		Cleans the pages and filters them regarding their length
		Parameters
		----------
		articles : DataFrame of all the articles 
		Returns
		-------
		Cleaned and filtered dataframe
		Examples
		--------
		>>> df = pd.read_csv('data.csv')
		>>> df_cleaned = filter_pages(df)
		"""

		from ast import literal_eval

		# Replace and split
		def replace_and_split(pages):
			for page in pages:
				page.replace("'s", " " "s").replace("\\n", "").split("'")
			return pages

		# Select pages with the required size
		def filter_on_size(pages, min_length=min_length, max_length=max_length):
			page_filtered = [
				page.strip()[:max_length]
				for page in pages
			]
			return page_filtered

		# Cleaning and filtering
		articles["pages"] = articles["pages"].apply(lambda x: literal_eval(str(x)))
		articles["pages"] = articles["pages"].apply(replace_and_split)
		articles["pages"] = articles["pages"].apply(filter_on_size)
		articles["pages"] = articles["pages"].apply(
			lambda x: x if len(x) > 0 else np.nan
		)

		# Read threshold for private dataset
		if not public_data:
			articles = articles.loc[articles["number_of_read"] >= read_threshold]

		# Drop empty articles
		if drop_empty:
			articles = articles.dropna(subset=["pages"]).reset_index(drop=True)

		return articles
