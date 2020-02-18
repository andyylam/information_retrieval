from skiplist import SkipList
import pickle


class Postings:
    def __init__(self, file_name):
        self.offset_to_postings = {}
        self.offset_to_postings[0] = set()
        self.file_name = file_name
        super().__init__()

    def clear_postings(self):
        all_postings = self.offset_to_postings[0]
        self.offset_to_postings = {0: all_postings}

    def get_postings_at_offset(self, offset):
        return self.offset_to_postings[offset]

    def add_doc_id(self, offset):
        if offset not in self.offset_to_postings:
            self.offset_to_postings[offset] = set()

    def add_docId_to_offset(self, offset, docId):
        self.offset_to_postings[offset].add(int(docId))
        if docId not in self.offset_to_postings[0]:
            self.offset_to_postings[0].add(int(docId))

    def save_to_file(self, dictionaries):
        with open(self.file_name, 'wb') as f:
            if 0 in self.offset_to_postings:
                f.seek(0)
                all_postings = SkipList.create_skip_list_from_list(
                    sorted(list(self.offset_to_postings[0])))
                f.write(pickle.dumps(all_postings))

            for term, node in dictionaries.get_dictionaries().items():
                offset = node[1]
                postings = SkipList.create_skip_list_from_list(
                    sorted(list(self.offset_to_postings[offset])))
                dictionaries.set_offset(term, f.tell())
                f.write(pickle.dumps(postings))

    def load_listing_at_offset(self, offset):
        with open(self.file_name, 'rb') as f:
            f.seek(offset)
            self.offset_to_postings[offset] = pickle.load(f)
