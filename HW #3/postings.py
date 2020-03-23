import pickle
import numpy as np
import math
from collections import Counter

# Posting class that stores all postings of all terms.
# Contains a mapping of `offset` associated to posting lists.
# Pickle is used to serialise and deserialise this class from disk.


class Postings:
    def __init__(self, file_name):
        self.offset_to_postings = {}
        self.file_name = file_name
        super().__init__()

    def clear_postings(self):
        self.offset_to_postings = {}

    def get_postings_at_offset(self, offset):
        return self.offset_to_postings[offset]

    def add_doc_id(self, offset):
        if offset not in self.offset_to_postings:
            self.offset_to_postings[offset] = []

    def add_docId_tf_to_offset(self, offset, docId, normalised_tf):
        self.offset_to_postings[offset].append((int(docId), normalised_tf))

    def save_to_file(self, dictionaries, collection_size):
        with open(self.file_name, 'wb') as f:
            for term, node in dictionaries.get_dictionaries().items():
                offset = node[1]
                # Sort the postings by docID
                postings = sorted(
                    self.offset_to_postings[offset], key=lambda x: x[0])
                # Sort the postings and store tuple: (idf, postings)
                postings = (math.log(collection_size /
                                     len(postings), 10), postings)
                # Set offset in dictionaries to the current byte offset of the postings storage file.
                dictionaries.set_offset(term, f.tell())
                f.write(pickle.dumps(postings))

    def load_listing_at_offset(self, offset):
        if offset not in self.offset_to_postings:
            with open(self.file_name, 'rb') as f:
                f.seek(offset)
                self.offset_to_postings[offset] = pickle.load(f)
