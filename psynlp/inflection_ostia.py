"""
Pipelines for SIGMORPHON-2017 task of Universal Morphological Inflection.
"""

import operator
import os
import networkx as nx
from helper_methods import *
import sys
import codecs
import string
import getopt
from functools import wraps


def fetch_input_output_pairs(language='english', quality='low'):
    filepath = "../daru-dataframe/spec/fixtures/{}-train-{}".format(
        language, quality)
    T = list()
    file = open(filepath, 'r')
    for line in file.readlines():
        source, dest, metadata = line.split("\t")
        if not "*" in source and not "*" in dest:
            metadata = metadata.strip("\n").split(";")
            T.append((source, metadata, dest))
            # print("{} + {} = {}".format(source, " + ".join(metadata), dest))
    print("Providing all words in structured manner, to OSTIA")
    T = sorted(T, key=operator.itemgetter(0))
    return T


def fetch_testing_data(language='english'):
    filepath = "../daru-dataframe/spec/fixtures/{}-dev".format(language)
    T = list()
    file = open(filepath, 'r')
    for line in file.readlines():
        source, expected_dest, metadata = line.split("\t")
        if not "*" in source and not "*" in expected_dest:
            metadata = metadata.strip("\n").split(";")
            T.append((source, metadata, expected_dest))
            # print("{} + {} = {}".format(source, " + ".join(metadata), dest))
    print("Providing all test words in structured manner, to OSTIA")
    T = sorted(T, key=operator.itemgetter(0))
    return T


def check_all_testing_data(model, lang, quality):
    c = n = 0
    l = {}
    T = fetch_testing_data(language=lang)
    for (source, metadatas, expected_dest) in T:
        predicted_dest, closest_word = model.fit_closest_path(
            source, metadatas)
        if predicted_dest == expected_dest:
            print("{} + {}: expected and received {}".format(source,
                                                             metadatas, predicted_dest))
            c += 1
        else:
            dist = mod_levenshtein(expected_dest, predicted_dest)
            if dist in l:
                l[dist] += 1
            else:
                l[dist] = 1
            print("{} + {}: expected {}, but received {}".format(source,
                                                                 metadatas, expected_dest, predicted_dest))
        print("Prediction given by most fitting path of word: {}".format(closest_word))
        n += 1
    print("\n\nExact word-match accuracy: {}". format(100.00*float(c)/float(n)))
    # print("\n Levenshtein distribution:", l)


lang = 'english'
quality = 'high'
T = fetch_input_output_pairs(language=lang, quality=quality)
T = OSTIA(T)

check_all_testing_data(T, lang, quality)
