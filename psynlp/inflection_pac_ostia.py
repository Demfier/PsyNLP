"""
Pipelines for SIGMORPHON-2017 task of Universal Morphological Inflection.
"""

import operator
import os
import networkx as nx
from helper_methods import *
from pac_library import *


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
        print(wordpairs)
        concept = init_concept_from_wordpairs(wordpairs)
        if len(concept.objects()) > 0:
            start1 = time.clock()
            pac = concept.pac_basis(concept.is_member, 0.1, 0.1)
            end1 = time.clock() - start1
        else:
            pac, end1 = None, None
        metadata_fca[metadata] = (concept, pac, end1)
    return(metadata_fca)


language = 'polish'
quality = 'high'
metadata_words = parse_metadata_words(language=language, quality=quality)
metadata_fca = parse_metadata_fca(metadata_words)
print(metadata_fca)
for metadata in metadata_fca:
    print(metadata)
    concept, pac, end1 = metadata_fca[metadata]
    j = 0
    if pac:
        for (antecedent_attrs, consequent_attrs) in pac:
            j += 1
            print("PAC Implication", j, ":", len(antecedent_attrs), "attributes:", " ->", len(consequent_attrs), "attributes with",
                  len(concept.attributes_extent(set(consequent_attrs))), "objects : ", concept.attributes_extent(set(consequent_attrs)))

        print("# of objects:", len(concept.objects()))
        print("# of attributes:", len(concept.attributes()))
        print("# of Implications:", len(pac))
        print(end1)

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
        print(len(consequent_attrs))
        ostia = ostia_regex.OSTIA(consequent_attrs)
        scores.append(ostia.matches_any_path(source))

    min_score, score_tup = sorted(scores, key=operator.itemgetter(0))[0]
    just_scores = [s for s, _ in scores]
    index_of_min_score = just_scores.index(min_score)
    _, cluster_words = list(cluster)[index_of_min_score]
    operations = concept.objects_intent(set(cluster_words))
    computed_dest = inflect(source, operations)
    if computed_dest == expected_dest:
        c += 1
        print("{} + {}: Expected and found {}".format(source, metadata, computed_dest))
    else:
        print("{} + {}: Expected {} but found {}".format(source,
                                                         metadata, expected_dest, computed_dest))
    print("due to {} with score {}".format(score_tup, min_score))
    n += 1
    # do operations
print(100*float(c) / n)
