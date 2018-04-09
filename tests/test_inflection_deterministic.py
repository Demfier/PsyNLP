import pytest
from ..psynlp import inflection_deterministic


def test_fetch_accuracy():
    languages = ['english', 'polish', 'bengali']
    qualities = ['low', 'medium', 'high']
    accuracies = []

    for language in languages:
        for quality in qualities:
            accuracies.append((language, quality, inflection_deterministic.fetch_accuracy(language=language, quality=quality)))
    print accuracies
    return True
