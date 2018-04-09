"""
Pipelines for SIGMORPHON-2017 task of Universal Morphological Inflection.
"""

from ..core.ostia import OSTIA
from ..helpers.importers import fetch_input_output_pairs, fetch_testing_data
from ..helpers.text import levenshtein


def fetch_accuracy(language='english', quality='high'):
    model = fetch_input_output_pairs(language=language, quality=quality)
    model = OSTIA(model)

    correct = total = 0
    levenshteinDist = {}
    T = fetch_testing_data(language=language)
    for (source, metadatas, expected_dest) in T:
        predicted_dest, closest_word = model.fit_closest_path(source, metadatas.split(";"))
        if predicted_dest is None:
            if source == expected_dest:
                correct += 1
            total += 1
            continue
        if predicted_dest == expected_dest:
            verbose_print_1("{} + {}: expected and received {}".format(source,
                                                             metadatas, predicted_dest))
            correct += 1
        else:
            dist = levenshtein(expected_dest, predicted_dest)[2]
            if dist in levenshteinDist:
                levenshteinDist[dist] += 1
            else:
                levenshteinDist[dist] = 1
            verbose_print_1("{} + {}: expected {}, but received {}".format(source,
                                                                 metadatas, expected_dest, predicted_dest))
        total += 1
    accuracy = 100.00*float(correct)/float(total)
    print("\n\nExact word-match accuracy for {}-{}: {}".format(language, quality, accuracy))
    return accuracy
