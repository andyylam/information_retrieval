from dictionaries import Dictionaries
from postings import Postings
from collections import Counter, defaultdict
from nltk import PorterStemmer, word_tokenize, sent_tokenize
import heapq
from utils import *

operators = {'OR': 1, 'AND': 2, 'NOT': 3}

#  Utility class that has high level methods to perform query parsing, query proessing and search operations


class Searcher:
    def __init__(self, dictionaries, postings):
        self.stemmer = PorterStemmer()
        self.dictionaries = dictionaries
        self.postings = postings
        super().__init__()

    def set_query(self, query):
        self.query = query

    # Function to calculate cosine score of all relevant documents and output the top 10 relevant documents, or less if there are less than 10 documents with non-zero score.
    def evaluate_query(self):
        scores = defaultdict(int)
        query_terms = []
        for sentence in sent_tokenize(self.query):
            for word in word_tokenize(sentence):
                query_terms.append(self.stemmer.stem(word=word.lower()))

        # Get mapping of terms to term frequency first, before computing term to weights
        term_to_weights = Counter(query_terms)

        for term in term_to_weights:
            if self.token_in_vocab(term):
                idf, postings_list = self.get_postings(term)
                query_tf = get_term_frequency_weight(term_to_weights[term])
                # Calculate weight with tf * idf and assign weight to term
                weight = idf * query_tf
                term_to_weights[term] = weight

        # Calculate the query vector length
        query_length = math.sqrt(
            sum(map(lambda x: x * x, dict(term_to_weights).values())))

        for term in term_to_weights:
            if self.token_in_vocab(term):
                _, postings_list = self.get_postings(term)
                for (docID, doc_tf) in postings_list:
                    # Add score for that document
                    scores[docID] += term_to_weights[term] * \
                        doc_tf / query_length

        # Get top 10 scoring documents with a heap
        heap = [(-value, key) for key, value in scores.items()]
        largest = heapq.nsmallest(10, heap)
        return ' '.join(map(lambda x: str(x[1]), largest))

    # Checks whether the token exists in the current dictionary.

    def token_in_vocab(self, token):
        return self.dictionaries.get_offset(token)

    # Loads the postings list to memory for a given token
    def load_postings(self, token):
        offset = self.dictionaries.get_offset(token)
        self.postings.load_listing_at_offset(offset)

    # Loads the postings list to memory for a given token and returns it.
    def get_postings(self, token):
        offset = self.dictionaries.get_offset(token)
        self.postings.load_listing_at_offset(offset)
        return self.postings.get_postings_at_offset(offset)

    # Clear postings from the searcher class.
    def clear_postings(self):
        self.postings.clear_postings()
