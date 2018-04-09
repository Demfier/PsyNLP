import pytest
from ..psynlp.pipelines import deterministic


def test_fetch_accuracy():
    """
    Tests the deterministic pipeline
    """
    languages = ['english', 'polish', 'bengali']
    qualities = ['low', 'medium', 'high']
    accuracies = []

    for language in languages:
        for quality in qualities:
            accuracies.append((language, quality, deterministic.fetch_accuracy(language=language, quality=quality)))
    print(accuracies)
    return True
