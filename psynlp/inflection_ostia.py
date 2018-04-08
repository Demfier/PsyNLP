"""
Pipelines for SIGMORPHON-2017 task of Universal Morphological Inflection.
"""

from ostia import OSTIA
from helper import fetch_input_output_pairs, fetch_testing_data, levenshtein

def fetch_accuracy(language='emglish', quality='high'):
    model = fetch_input_output_pairs(language=language, quality=quality)
    model = OSTIA(model)

    correct = total = 0
    levenshteinDist = {}
    T = fetch_testing_data(language=language)
    for (source, metadatas, expected_dest) in T:
        predicted_dest, closest_word = model.fit_closest_path(source, metadatas)
        if predicted_dest == expected_dest:
            print("{} + {}: expected and received {}".format(source,
                                                             metadatas, predicted_dest))
            correct += 1
        else:
            dist = levenshtein(expected_dest, predicted_dest)[2]
            if dist in levenshteinDist:
                levenshteinDist[dist] += 1
            else:
                levenshteinDist[dist] = 1
            print("{} + {}: expected {}, but received {}".format(source,
                                                                 metadatas, expected_dest, predicted_dest))
        # print("Prediction given by most fitting path of word: {}".format(closest_word))
        total += 1
    accuracy = 100.00*float(correct)/float(total)
    print("\n\nExact word-match accuracy: {}".format(accuracy))
    return accuracy
