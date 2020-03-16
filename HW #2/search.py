#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import gc
from nltk import PorterStemmer
from dictionaries import Dictionaries
from postings import Postings
from searcher import Searcher


def usage():
    print("usage: " +
          sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")


def run_search(dict_file, postings_file, queries_file, results_file):
    """
    Using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('Running search on the queries...')

    dictionaries = Dictionaries(dict_file)
    dictionaries.load()
    postings = Postings(postings_file)
    searcher = Searcher(dictionaries, postings)

    result_string = ''
    with open(queries_file, 'r') as f, open(results_file, 'w') as o:
        for i, query in enumerate(f):
            searcher.set_query(query.strip())
            output = searcher.evaluate_query()
            result_string += output.strip() + '\n'
            searcher.clear_postings()
            # Explicitly call the garbage collector to free up memory of unreferenced objects.
            gc.collect()
        f.close()
        o.write(result_string.strip())
        o.close()


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None:
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
