"""
Pipelines for SIGMORPHON-2017 task of Universal Morphological Inflection.
"""

import pandas as pd
from ..core.ostia import OSTIA
from ..helpers.importers import init_concept_from_wordpairs, fetch_testing_data, parse_metadata_words, parse_metadata_fca
from ..helpers.text import inflect


def fetch_accuracy(language='english', quality='high'):
    pac = parse_metadata_fca(parse_metadata_words(
        language=language, quality=quality), 'deterministic')
    testing_data = fetch_testing_data(language=language)
    total = correct = 0

    for (source, metadata, expected_dest) in testing_data:
        scores = []
        if metadata not in pac:
            if source == expected_dest:
                correct += 1
            total += 1
            continue

        concept, cluster, _ = pac[metadata]
        if not cluster:
            if source == expected_dest:
                correct += 1
            total += 1
            continue

        for (antecedent_attrs, consequent_attrs) in cluster:
            ostia = OSTIA(consequent_attrs)
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

        computed_dest = inflect(source, operations)

        if computed_dest == expected_dest:
            correct += 1
            verbose_print_1("{} + {}: Expected and found {}".format(source, metadata, computed_dest))
        else:
            verbose_print_1("{} + {}: Expected {} but found {}".format(source, metadata, expected_dest, computed_dest))
        if closest_word:
            verbose_print_2("due to {} with score {}".format(closest_word, min_score))
        total += 1

    if total == 0:
        total = 1
    accuracy = 100*float(correct) / total
    print("\n\nExact word-match accuracy for {}-{}: {}".format(language, quality, accuracy))
    return accuracy
