from ..psynlp.pipelines import ostia
from ..psynlp.helpers import builtins
builtins.init_verbose(1)


def test_fetch_accuray():
    """
    Tests the ostia pipeline
    """
    languages = ['english', 'polish', 'bengali']
    qualities = ['low', 'medium']
    accuracies = []

    for quality in qualities:
        for language in languages:
            accuracies.append((language, quality, ostia.fetch_accuracy(language=language, quality=quality)))
    print(accuracies)
    return True
