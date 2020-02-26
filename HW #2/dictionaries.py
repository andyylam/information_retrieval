import pickle


# Dictionary class that stores all terms.
# Contains a mapping of `terms` to (term, offset).
# Pickle is used to serialise and deserialise this class from disk.

class Dictionaries:
    def __init__(self, file_name):
        self.dict = {}
        self.file_name = file_name
        super().__init__()

    def add_term(self, term, offset):
        self.dict[term] = (0, offset)

    def get_offset(self, term):
        if term in self.dict:
            return self.dict[term][1]

    def set_offset(self, term, offset):
        self.dict[term] = (self.dict[term][0], offset)

    def increment_frequency(self, term):
        if term in self.dict:
            self.dict[term] = (self.dict[term][0] + 1, self.dict[term][1])

    def get_dictionaries(self):
        return self.dict

    def has_term(self, term):
        return term in self.dict

    def save_to_file(self):
        with open(self.file_name, 'wb') as f:
            pickle.dump(self.dict, f)
            f.close()

    def load(self):
        with open(self.file_name, 'rb') as f:
            self.dict = pickle.load(f)
            f.close()
