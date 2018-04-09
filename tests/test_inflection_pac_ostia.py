import pytest
from ..psynlp import inflection_pac_ostia


def test_fetch_accuracy():
    print(inflection_pac_ostia.fetch_accuracy(language='english', quality='high'))
