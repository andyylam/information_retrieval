#!/usr/bin/python3
import re
import sys
import getopt
import os
import math
from collections import Counter
from nltk import sent_tokenize, word_tokenize, PorterStemmer

from dictionaries import Dictionaries
from postings import Postings
from utils import get_term_frequency_weight


def usage():
    print("usage: " +
          sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")


def build_index(in_dir, out_dict, out_postings):
    """
    Build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('Indexing...')

    stemmer = PorterStemmer()
    dictionaries = Dictionaries(out_dict)
    postings = Postings(out_postings)
    offset = 1
    count = len(os.listdir(in_dir))

    for docID in os.listdir(in_dir):
        f = open(f'{in_dir}/{docID}', 'r')
        content = f.read()
        sentences = sent_tokenize(content)
        doc_terms = []
        for sentence in sentences:
            for word in word_tokenize(sentence):
                term = stemmer.stem(word=word.lower())
                doc_terms.append(term)

        # Calculate weighted term frequencies for each term
        weighted_term_freqs = [(x[0], get_term_frequency_weight(x[1]))
                               for x in Counter(doc_terms).most_common()]
        # Calculate document vector length
        doc_length = math.sqrt(
            sum(map(lambda x: x[1] * x[1], weighted_term_freqs)))

        for term, normalised_tf in weighted_term_freqs:
            if dictionaries.has_term(term):
                old_offset = dictionaries.get_offset(term)
                postings.add_docId_tf_to_offset(
                    old_offset, docID, normalised_tf / doc_length)
            else:
                dictionaries.add_term(term, offset)
                postings.add_doc_id(offset)
                postings.add_docId_tf_to_offset(
                    offset, docID, normalised_tf / doc_length)
                offset += 1

    postings.save_to_file(dictionaries, count)
    dictionaries.save_to_file()


sys.setrecursionlimit(100000)
input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # input directory
        input_directory = a
    elif o == '-d':  # dictionary file
        output_file_dictionary = a
    elif o == '-p':  # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
