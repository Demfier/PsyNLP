"""
Pipelines for SIGMORPHON-2017 task of Universal Morphological Inflection.
"""

import operator
import os
import networkx as nx
from helper_methods import *
from pac_library import *
import _pickle as pickle
import ostia_regex
import pandas as pd


def fetch_testing_data(language='english'):
    filepath = "../daru-dataframe/spec/fixtures/{}-dev".format(language)
    T = list()
    file = open(filepath, 'r')
    for line in file.readlines():
        source, expected_dest, metadata = line.split("\t")
        if not "*" in source and not "*" in expected_dest:
            metadata = metadata.strip("\n")
            T.append((source, metadata, expected_dest))
            # print("{} + {} = {}".format(source, " + ".join(metadata), dest))
    print("Providing all test words in structured manner")
    T = sorted(T, key=operator.itemgetter(0))
    return T


def parse_metadata_words(language='english', quality='low'):
    metadata_words = {}
    filepath = "../daru-dataframe/spec/fixtures/{}-train-{}".format(
        language, quality)
    file = open(filepath, 'r')
    for line in file.readlines():
        source, dest, metadata = line.split("\t")
        if not "*" in source and not "*" in dest:
            metadata = metadata.strip()
            if metadata in metadata_words:
                metadata_words[metadata].append((source, dest))
            else:
                metadata_words[metadata] = []
    return(metadata_words)


def parse_metadata_fca(metadata_words):
    metadata_fca = {}
    for metadata in metadata_words:
        wordpairs = metadata_words[metadata]
        concept = init_concept_from_wordpairs(wordpairs)
        if len(concept.objects()) > 0:
            start1 = time.clock()
            pac = deterministic_pac(concept)
            end1 = time.clock() - start1
        else:
            pac, end1 = None, None
        metadata_fca[metadata] = (concept, pac, end1)
    return(metadata_fca)


def inflect(word, operations):
    for operation in sorted(operations):
        method, chunk = operation.split('_')
        if method == 'delete':
            word = word.rstrip(chunk)
        else:
            word = word + chunk
    return word


def deterministic_pac(concept):
    def generate_df(concept):
        rows = []
        for word in concept.attributes():
            operations = sorted(list(concept.objects_intent(set([word]))))
            details = dict()
            details['source'] = word
            details['operations'] = ','.join(operations)
            rows.append(details)

        df = pd.DataFrame(rows)
        return df

    def structure_df_to_pac(df):
        pac = list()
        for (operations, sub_df) in sorted(df.groupby(['operations']), key=lambda x: len(list(x[1]['source'])), reverse=True):
            # for (operations, sub_df) in sorted(df.groupby(['operations'])):
            consequent_attrs = tuple(sorted(list(sub_df['source'])))
            antecedent_attrs = tuple([consequent_attrs[0]])
            pac.append((antecedent_attrs, consequent_attrs))

        return pac

    df = generate_df(concept)
    pac = structure_df_to_pac(df)
    return pac


language = 'english'
quality = 'high'
metadata_words = parse_metadata_words(language=language, quality=quality)

pac = parse_metadata_fca(metadata_words)
testing_data = fetch_testing_data(language=language)
n = c = 0

for (source, metadata, expected_dest) in testing_data:
    scores = []
    if metadata not in pac:
        continue
    concept, cluster, _ = pac[metadata]
    if not cluster:
        continue

    for (antecedent_attrs, consequent_attrs) in cluster:
        ostia = ostia_regex.OSTIA(consequent_attrs)
        scores.append((consequent_attrs, ostia.matches_any_path(source)))

    scores = sorted(scores, key=lambda x: x[1][0])
    cluster_words, (min_score, closest_word) = scores[0]
    just_scores = [s[0] for _, s in scores]

    if just_scores.count(min_score) == 1:
        operations = concept.objects_intent(set(cluster_words))
    else:
        max_operations = 0
        index_of_min_score = 0
        for i, s in enumerate(scores[0:just_scores.count(min_score)]):
            this_cluster, (score, _) = s
            operations = concept.objects_intent(set(this_cluster))
            if len(operations) > max_operations:
                max_operations = len(operations)
                cluster_words = this_cluster
                index_of_min_score = i
        closest_word = scores[index_of_min_score][1][1]
        operations = concept.objects_intent(set(cluster_words))
        print(len(operations))

    computed_dest = inflect(source, operations)
    if computed_dest == expected_dest:
        c += 1
        print("{} + {}: Expected and found {}".format(source, metadata, computed_dest))
    else:
        print("{} + {}: Expected {} but found {}".format(source,
                                                         metadata, expected_dest, computed_dest))
    print("due to {} with score {}".format(closest_word, min_score))
    n += 1
    # do operations
if n == 0:
    n = 1
print(100*float(c) / n)
