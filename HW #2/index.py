#!/usr/bin/python3
import re
import sys
import getopt
import os
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from dictionaries import Dictionaries
from postings import Postings


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

    for docID in os.listdir(in_dir):
        f = open(f'{in_dir}/{docID}', 'r')
        content_tokens = word_tokenize(f.read())
        for word in content_tokens:
            term = stemmer.stem(word=word).lower()

            if dictionaries.has_term(term):
                old_offset = dictionaries.get_offset(term)
                postings.add_docId_to_offset(old_offset, docID)
            else:
                dictionaries.add_term(term, offset)
                postings.add_doc_id(offset)
                postings.add_docId_to_offset(offset, docID)
                offset += 1

            dictionaries.increment_frequency(term)

    postings.save_to_file(dictionaries)
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
