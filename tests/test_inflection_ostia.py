import pytest
from ..psynlp import inflection_ostia


def test_fetch_accuray():
    print(inflection_ostia.fetch_accuracy(language='english', quality='low'))

    languages = ['english', 'polish', 'bengali']
    qualities = ['low', 'medium', 'high']
    accuracies = []

    for language in languages:
        for quality in qualities:
            accuracies.append((language, quality, inflection_ostia.fetch_accuracy(language=language, quality=quality)))
    print(accuracies)
    return True
