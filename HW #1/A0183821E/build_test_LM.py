#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import nltk
import sys
import getopt
from collections import defaultdict
import math

OTHER = 'other'         # Represents string printed when all LMs don't fit
WINDOW_SIZE = 4         # Quadgram
THRESHOLD_VALUE = 0.37   # Threshold value used to determine whether any LMs fit


def build_LM(in_file):
    """
    Build language models for each label.
    Each line in `in_file` contains a label and a string separated by a space.
    Language model is represented with a nested dictionary in the following format:
    model = { 
        {language} (str): {
            {quadgram_token} (tuple): {count} (int)
            ...
        }
    }
    """

    print('Building language models...')
    training_set = open(in_file)

    model = defaultdict(lambda: defaultdict(int))

    for line in training_set:
        language, text = parseLine(line)
        # Use nltk.ngrams() to generate character quadgrams
        quadgrams = nltk.ngrams(text, WINDOW_SIZE,  pad_left=True,
                                pad_right=True, left_pad_symbol='<START>', right_pad_symbol='<END>')
        for token in list(quadgrams):
            model[language][token] += 1
    training_set.close()
    # Apply add one smoothing to the model, and then convert it into a probablistic model
    model = countToProbabilityModel(laplaceSmoothing(model))
    return model


def countToProbabilityModel(model):
    """
    Converts the count model to a probabilistic model.
    Simply divides count of each token with the total vocabulary count of the model.
    """
    for lang in model:
        total_count = float(sum(model[lang].values()))
        for tokens in model[lang]:
            model[lang][tokens] /= total_count
    return model


def laplaceSmoothing(model):
    """
    Applies Laplace (add-one) smoothing to the model
    """

    # Add one to all seen values
    new_model = {
        lang: {
            tokens: count+1
            for tokens, count in outer.items()
        }
        for lang, outer in model.items()
    }

    for language, words in new_model.items():
        current_language_vocab = set(words)
        for other_languages in filter(lambda l: l != language, new_model):
            # Unseen set contains tokens in the other language but not in current one
            unseen = set(new_model[other_languages].keys()
                         ).difference(current_language_vocab)
            for w in unseen:
                new_model[language][w] = 1
    return new_model


def parseLine(line):
    """
    Helper function to parse line from training input.
    All characters are lowercased. 
    Returns (language, text)
    """
    line = line.strip().lower()
    indexOfFirstSpace = line.find(' ')
    return line[:indexOfFirstSpace], list(line[indexOfFirstSpace+1:])


def test_LM(in_file, out_file, model):
    """
    Test the language models on new strings
    Each line of in_file contains a string
    Prints the most probable label for each string into out_file
    """
    print("Testing language models...")

    new_data = open(in_file)
    output = open(out_file, 'a')

    for line in new_data:
        lang_probs = defaultdict(int)
        line = line.strip().lower()
        quadgrams = set(nltk.ngrams(line, WINDOW_SIZE,  pad_left=True,
                                    pad_right=True, left_pad_symbol='<START>', right_pad_symbol='<END>'))

        for lang in model:
            probability, lang_vocab = 0, set(model[lang].keys())
            # Common tokens contains tokens in quadgrams that are also in the current LM
            common_tokens = quadgrams.intersection(lang_vocab)
            for token in common_tokens:
                # Using logarithm because probabilities become too small
                probability += math.log(model[lang][token])
            lang_probs[lang] = probability

        predictedLanguage = max(lang_probs, key=lang_probs.get)
        # Calculate propotion of tokens that are not in the LM
        proportion_missing = 1 - \
            float(len(common_tokens)) / float(len(quadgrams))
        # If proportion of tokens of missing exceeds specified THRESHOLD_VALUE, then LM contains insufficient information and therefore the predicted language is OTHER
        if proportion_missing > THRESHOLD_VALUE:
            predictedLanguage = OTHER
        output.write(predictedLanguage + '\n')

    new_data.close()
    output.close()


def usage():
    print("usage: " +
          sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file")


input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
