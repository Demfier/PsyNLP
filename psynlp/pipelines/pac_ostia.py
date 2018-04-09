"""
Pipelines for SIGMORPHON-2017 task of Universal Morphological Inflection.
"""

import operator
from ..core.ostia import OSTIA
from ..helpers.importers import parse_metadata_fca, parse_metadata_words, fetch_testing_data
from ..helpers.text import inflect


def fetch_accuracy(language='english', quality='high'):
    pac = parse_metadata_fca(parse_metadata_words(
        language=language, quality=quality), 'pac')
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
            scores.append(ostia.matches_any_path(source))

        min_score, score_tup = sorted(scores, key=operator.itemgetter(0))[0]
        just_scores = [s for s, _ in scores]
        index_of_min_score = just_scores.index(min_score)
        _, cluster_words = list(cluster)[index_of_min_score]
        operations = concept.objects_intent(set(cluster_words))
        computed_dest = inflect(source, operations)
        if computed_dest == expected_dest:
            correct += 1
            verbose_print_1("{} + {}: Expected and found {}".format(source,
                                                          metadata, computed_dest))
        else:
            verbose_print_1("{} + {}: Expected {} but found {}".format(source,
                                                             metadata, expected_dest, computed_dest))
        verbose_print_2("due to {} with score {}".format(score_tup, min_score))
        total += 1

    accuracy = 100*float(correct) / total
    print("\n\nExact word-match accuracy for {}-{}: {}".format(language, quality, accuracy))
    return accuracy
