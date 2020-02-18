from dictionaries import Dictionaries
from postings import Postings
from skiplist import SkipList
from collections import deque
from nltk import PorterStemmer

operators = {'OR': 1, 'AND': 2, 'NOT': 3}


class Searcher:
    stemmer = PorterStemmer()

    def __init__(self, dictionaries, postings):
        self.dictionaries = dictionaries
        self.postings = postings
        self.postings.load_listing_at_offset(0)
        super().__init__()

    def set_query(self, query):
        self.query = query

    def evaluate_query(self):
        output_queue = self.get_postfix_expression(
            self.parse_query(self.query))
        return self.process_query(output_queue).to_string()

    def token_in_vocab(self, token):
        return self.dictionaries.get_offset(token)

    def get_postings(self, token):
        offset = self.dictionaries.get_offset(token)
        self.postings.load_listing_at_offset(offset)
        return self.postings.get_postings_at_offset(offset)

    def process_query(self, expression):
        stack = []
        exp = deque(expression)
        while exp:
            token = exp.popleft()
            if token in operators:
                if token == 'NOT':
                    complement_postings = stack.pop()
                    if exp and exp[0] == 'AND':
                        next_operator = exp.popleft()
                        stack.append(self.evaluate_and_not_query(
                            complement_postings, stack.pop()))
                    else:
                        all_postings = self.postings.get_postings_at_offset(0)
                        stack.append(self.evaluate_and_not_query(
                            complement_postings, all_postings))
                else:
                    postings1, postings2 = stack.pop(), stack.pop()
                    if token == 'AND':
                        stack.append(self.evaluate_and_query(
                            postings1, postings2))
                    elif token == 'OR':
                        stack.append(self.evaluate_or_query(
                            postings1, postings2))
            else:
                if self.token_in_vocab(token) is None:
                    stack.append(SkipList(None))
                else:
                    stack.append(self.get_postings(token))
        return stack.pop()

    def evaluate_and_not_query(self, complement_postings, postings):
        return SkipList.intersection_complement(complement=complement_postings, other=postings)

    def evaluate_and_query(self, postings1, postings2):
        return SkipList.intersection(postings1, postings2)

    def evaluate_or_query(self, postings1, postings2):
        return SkipList.union(postings1, postings2)

    def parse_query(self, query):
        output = []
        for token in query.split(" "):
            if token[0] == '(':
                output.append('(')
                output.append(Searcher.stemmer.stem(word=token[1:]).lower())
            elif token[-1] == ')':
                output.append(Searcher.stemmer.stem(token[:-1]).lower())
                output.append(')')
            elif token in operators:
                output.append(token)
            else:
                output.append(Searcher.stemmer.stem(token).lower())
        return output

    def get_postfix_expression(self, tokens):
        operator_stack, output_queue = [], []
        for token in tokens:
            if token in operators:
                while operator_stack and operator_stack[-1] != '(' and operators[operator_stack[-1]] > operators[token]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
            else:
                output_queue.append(token)
        while operator_stack:
            output_queue.append(operator_stack.pop())
        print(output_queue)
        return output_queue

    def clear_postings(self):
        self.postings.clear_postings()
