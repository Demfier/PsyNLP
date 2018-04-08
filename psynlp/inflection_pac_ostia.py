"""
Pipelines for SIGMORPHON-2017 task of Universal Morphological Inflection.
"""

import operator
from ..psynlp.ostia import OSTIA
from ..psynlp.helper import parse_metadata_fca, parse_metadata_words, fetch_testing_data, inflect


def fetch_accuracy(language='english', quality='high'):
    pac = parse_metadata_fca(parse_metadata_words(
        language=language, quality=quality), 'pac')
    testing_data = fetch_testing_data(language=language)
    total = correct = 0

    for (source, metadata, expected_dest) in testing_data:
        scores = []
        if metadata not in pac:
            continue
        concept, cluster, _ = pac[metadata]
        if not cluster:
            continue
        for (antecedent_attrs, consequent_attrs) in cluster:
            print(len(consequent_attrs))
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
            print("{} + {}: Expected and found {}".format(source,
                                                          metadata, computed_dest))
        else:
            print("{} + {}: Expected {} but found {}".format(source,
                                                             metadata, expected_dest, computed_dest))
        print("due to {} with score {}".format(score_tup, min_score))
        total += 1

    accuracy = 100*float(correct) / total
    print(accuracy)
    return accuracy
