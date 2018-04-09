import pytest
from ..psynlp.pipelines import ostia


def test_fetch_accuray():
    print(ostia.fetch_accuracy(language='english', quality='low'))
