import math
import numpy as np

# Utility class that has low level methods for tf x idf calculations


def get_term_frequency_weight(tf):
    if not tf:
        return 0
    return 1 + math.log(tf, 10)


def get_inverse_doc_frequency(total, df):
    if not df:
        return 0
    return math.log(total / df, 10)


def tfxidf(x, df):
    return get_term_frequency_weight(x) * get_inverse_doc_frequency(df)
