import pytest
from ..psynlp import inflection_ostia


def test_fetch_accuray():
    print(inflection_ostia.fetch_accuracy(language='english', quality='low'))
