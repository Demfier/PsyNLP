import pytest
from ..psynlp import inflection_deterministic


def test_fetch_accuray():
    print(inflection_deterministic.fetch_accuracy(language='english', quality='low'))
